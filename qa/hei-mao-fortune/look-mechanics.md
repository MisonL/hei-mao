# Fortune look mechanics

The Fortune role keeps the lower body, feet, red-and-gold outfit contact, grain basket contact, and pumpkin contact anchored while the head and upper torso lead the gaze. The eyes, eyelids, snout, and ear angles follow the head turn. The heart mitts and grain basket are rigid attached props: they follow the torso with a small lag on diagonal turns and remain connected at every direction. The basket stays on the screen-right side and the pumpkin stays on the screen-left side without changing size or crossing the body.

Cardinal pose families use viewer coordinates:

- 000 up: chin lifts, eyelids open toward the upper edge, ears rise slightly, and the lower body remains grounded.
- 090 screen-right: snout, pupils, head, and upper torso turn right; the right-facing side becomes more visible and the opposite ear is partly occluded.
- 180 down: chin lowers, eyelids and pupils aim toward the lower edge, and the red-and-gold outfit and props remain attached to the grounded torso.
- 270 screen-left: snout, pupils, head, and upper torso turn left; the left-facing side becomes more visible and the opposite ear is partly occluded.

Intermediate directions interpolate the head turn, eye aim, ear follow-through, torso lean, and small prop lag in equal visual steps. The lower-body anchor and apparent body height stay constant. No whole-sprite rotation, replacement eyes, detached effects, labels, or background marks are allowed.

Motion budget: adjacent 22.5-degree steps use a small, even change in head angle and eye direction. Diagonals combine the neighboring cardinal pose families; they do not introduce a new gesture or a larger scale change. The final 337.5 pose must be one step before the approved 000 pose, and 157.5 must be one step before 180.
