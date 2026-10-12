#include "../src/swipe_motion.hpp"
#include <cassert>
#include <cmath>

int main() {
    assert(!HTSwipeMotion::outside_deadzone(1, 1, 16));
    assert(!HTSwipeMotion::outside_deadzone(10, 10, 16));
    assert(HTSwipeMotion::outside_deadzone(16, 0, 16));
    assert(HTSwipeMotion::outside_deadzone(0, -300, 16));
    assert(!HTSwipeMotion::outside_deadzone(25, 25, 40));
    assert(HTSwipeMotion::outside_deadzone(40, 0, 40));

    // The rendered offset depends on net displacement, not clamped steps.
    const double start = -500, scale = 4, min = -1000, max = 0;
    assert(HTSwipeMotion::clamp_axis(start, 200, scale, min, max) == 0);
    assert(HTSwipeMotion::clamp_axis(start, 0, scale, min, max) == start);
    assert(HTSwipeMotion::clamp_axis(start, -200, scale, min, max) == -1000);
    assert(HTSwipeMotion::clamp_axis(start, 25, scale, min, max) == -400);

    // At the edge, a clockwise or counter-clockwise loop must go home.
    const double edge = 0;
    assert(HTSwipeMotion::clamp_axis(edge, 0, scale, min, max) == edge);
    assert(HTSwipeMotion::clamp_axis(edge, 300, scale, min, max) == edge);
    return 0;
}
