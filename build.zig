const std = @import("std");

fn addExe(
    b: *std.Build,
    name: []const u8,
    source: []const u8,
    target: std.Build.ResolvedTarget,
    optimize: std.builtin.Optimize,
) *std.Build.Step.Compile {
    const mod = b.createModule(.{
        .root_source_file = b.path(source),
        .target = target,
        .optimize = optimize,
    });
    return b.addExecutable(.{ .name = name, .root_module = mod });
}

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const executables = [_][2][]const u8{
        .{ "verify_manifest_zig", "src/main.zig" },
        .{ "footprint_zig", "src/footprint.zig" },
        .{ "byotc_audit_zig", "src/byotc_audit.zig" },
    };
    for (executables) |spec| {
        b.installArtifact(addExe(b, spec[0], spec[1], target, optimize));
    }

    const test_step = b.step("test", "Run unit tests");
    const sources = [_][]const u8{ "src/main.zig", "src/footprint.zig", "src/byotc_audit.zig" };
    for (sources) |source| {
        const test_mod = b.createModule(.{
            .root_source_file = b.path(source),
            .target = target,
            .optimize = optimize,
        });
        const unit_tests = b.addTest(.{ .root_module = test_mod });
        test_step.dependOn(&b.addRunArtifact(unit_tests).step);
    }
}
