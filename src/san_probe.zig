const std = @import("std");

var global_io: std.Io = undefined;

fn out(allocator: std.mem.Allocator, comptime fmt: []const u8, args: anytype) !void {
    const text = try std.fmt.allocPrint(allocator, fmt, args);
    defer allocator.free(text);
    try std.Io.File.stdout().writeStreamingAll(global_io, text);
}

fn decide(allow: std.json.Value, dns: []const u8) bool {
    if (allow != .array) return false;
    for (allow.array.items) |item| {
        if (item != .string) continue;
        if (std.ascii.eqlIgnoreCase(item.string, dns)) return true;
    }
    return false;
}

pub fn main(init: std.process.Init) !void {
    const allocator = init.arena.allocator();
    global_io = init.io;
    const args = try init.minimal.args.toSlice(allocator);
    if (args.len < 2) {
        try out(allocator, "uso: san_probe_zig <san_frontera.json>\n", .{});
        std.process.exit(2);
    }

    const data = try std.Io.Dir.cwd().readFileAlloc(
        global_io, args[1], allocator, std.Io.Limit.limited(16 * 1024 * 1024)
    );
    const parsed = try std.json.parseFromSlice(std.json.Value, allocator, data, .{});
    defer parsed.deinit();

    const obj = parsed.value.object;
    const allow = obj.get("allowlist") orelse .null;
    const casos = obj.get("casos") orelse {
        try out(allocator, "faltan casos\n", .{});
        std.process.exit(2);
    };

    try out(allocator, "| ID | SAN | Veredicto |\n|---|---|---|\n", .{});
    var accepted: usize = 0;
    for (casos.array.items) |item| {
        const c = item.object;
        const id = c.get("id") orelse continue;
        const dns = c.get("dns") orelse continue;
        const ok = decide(allow, dns.string);
        if (ok) accepted += 1;
        try out(allocator, "| {s} | {s} | {s} |\n", .{
            id.string, dns.string, if (ok) "ACCEPTED" else "REJECTED",
        });
    }
    try out(allocator, "aceptados={d} | regla=lower+exacto\n", .{accepted});
}

test "decide ignora mayusculas" {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const parsed = try std.json.parseFromSlice(std.json.Value, arena.allocator(), "[\"edge.lab.local\"]", .{});
    defer parsed.deinit();
    try std.testing.expect(decide(parsed.value, "EDGE.LAB.LOCAL"));
    try std.testing.expect(!decide(parsed.value, "edge.lab.local."));
}
