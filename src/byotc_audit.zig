const std = @import("std");

var global_io: std.Io = undefined;

fn out(allocator: std.mem.Allocator, comptime fmt: []const u8, args: anytype) !void {
    const text = try std.fmt.allocPrint(allocator, fmt, args);
    defer allocator.free(text);
    try std.Io.File.stdout().writeStreamingAll(global_io, text);
}

fn inList(list: std.json.Value, needle: []const u8) bool {
    if (list != .array) return false;
    for (list.array.items) |item| {
        if (item != .string) continue;
        if (std.ascii.eqlIgnoreCase(item.string, needle)) return true;
    }
    return false;
}

pub fn main(init: std.process.Init) !void {
    const allocator = init.arena.allocator();
    global_io = init.io;
    const args = try init.minimal.args.toSlice(allocator);
    if (args.len < 3) {
        try out(allocator, "uso: byotc_audit_zig <config.json> <certs.json>\n", .{});
        std.process.exit(2);
    }

    const cfg_data = try std.Io.Dir.cwd().readFileAlloc(
        global_io, args[1], allocator, std.Io.Limit.limited(16 * 1024 * 1024)
    );
    const cfg_parsed = try std.json.parseFromSlice(std.json.Value, allocator, cfg_data, .{});
    defer cfg_parsed.deinit();
    const cfg = cfg_parsed.value.object;

    const certs_data = try std.Io.Dir.cwd().readFileAlloc(
        global_io, args[2], allocator, std.Io.Limit.limited(16 * 1024 * 1024)
    );
    const certs_parsed = try std.json.parseFromSlice(std.json.Value, allocator, certs_data, .{});
    defer certs_parsed.deinit();

    const ca_bundle = cfg.get("ca_bundle") orelse .null;
    const allow = cfg.get("allowlist") orelse .null;
    const flags = cfg.get("flags") orelse .null;
    const allow_len: usize = if (allow == .array) allow.array.items.len else 0;

    var accepted: usize = 0;
    try out(allocator, "| Certificado | Veredicto | Motivo |\n|---|---|---|\n", .{});
    for (certs_parsed.value.array.items) |item| {
        const cert = item.object;
        const id = cert.get("id") orelse continue;
        const issuer_v = cert.get("issuer") orelse continue;
        var verdict: []const u8 = "REJECTED";
        var reason: []const u8 = "chain_rejected";

        if (inList(ca_bundle, issuer_v.string)) {
            if (allow_len == 0) {
                const escape = flags == .object and flags.object.get("allow_no_mtls_allowlist") != null;
                if (escape) {
                    verdict = "ACCEPTED";
                    reason = "lab_escape_empty_allowlist";
                } else {
                    reason = "fail_closed_empty_allowlist";
                }
            } else {
                const dns = cert.get("san_dns") orelse .null;
                if (dns == .array) {
                    for (dns.array.items) |d| {
                        if (d == .string and inList(allow, d.string)) {
                            verdict = "ACCEPTED";
                            reason = "san_dns_allowlisted";
                            break;
                        }
                    }
                }
                if (std.mem.eql(u8, verdict, "REJECTED")) {
                    const ips = cert.get("san_ip") orelse .null;
                    if (ips == .array and ips.array.items.len > 0) {
                        reason = "san_ip_not_compared";
                    } else {
                        reason = "san_not_allowlisted";
                    }
                }
            }
        }

        if (std.mem.eql(u8, verdict, "ACCEPTED")) accepted += 1;
        try out(allocator, "| {s} | {s} | {s} |\n", .{ id.string, verdict, reason });
    }
    try out(allocator, "aceptados={d} | tecnica=B-07 BYOTC-SAN\n", .{accepted});
}

test "inList insensible a mayusculas" {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const parsed = try std.json.parseFromSlice(std.json.Value, arena.allocator(), "[\"EDGE.LAB.LOCAL\"]", .{});
    defer parsed.deinit();
    try std.testing.expect(inList(parsed.value, "edge.lab.local"));
}
