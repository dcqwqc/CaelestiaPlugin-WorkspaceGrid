#pragma once

// Small, independent gesture primitives; kept unit-testable without Hyprland.
struct HTSwipeMotion {
    static bool outside_deadzone(double x, double y, double pixels) {
        return x * x + y * y >= pixels * pixels;
    }

    static double clamp_axis(double origin, double delta, double scale,
                             double min, double max) {
        const double v = origin + delta * scale;
        return v < min ? min : (v > max ? max : v);
    }
};
