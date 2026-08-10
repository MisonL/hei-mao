# hei-mao-delivery look mechanics

## Character construction

The delivery character is a compact dark-brown pig mascot with a square head, pink ears and snout, white fine-stripe shirt, blue overalls, red heart gloves, white shoes, a coral-orange delivery vest, a teal insulated delivery bag, and a small attached grocery bag. The shoe soles, lower blue overalls, and vest hem are the grounded registration anchor. The bags and grocery bag remain physically attached to the torso and do not float or change size independently.

## Natural look motion

- The head plane and pink snout lead the gaze. Turn or pitch the face toward the target while preserving the original square head, ear, snout, eye, outline, and body proportions.
- The eyes and eyelids follow the head direction with small natural changes. Do not slide replacement pupils across a fixed face, add googly eyes, or redesign the eye construction.
- The ears follow the head with a small continuous lag. They may reveal a little more side surface but must stay attached and keep their original size.
- The shoulders and upper torso follow subtly. The vest, straps, overalls, gloves, shoes, delivery bag, and grocery bag stay attached; the shoe baseline, vest hem, lower torso, and bag connection points remain registered.
- Do not introduce food, tools, text, symbols, motion marks, shadows, glows, or detached effects in look cells. The delivery props already present remain the only props.

## Cardinal pose families

- `000` up: pitch the head, snout, and eyes toward the top edge; reveal a little more lower face or chin while the feet, vest hem, and bags stay anchored.
- `090` screen-right: yaw the head and snout toward the viewer's right. The snout tip, pupils, and front face edge must read on the screen-right side of the head center; the torso follows only slightly.
- `180` down: pitch the head, snout, and eyes toward the bottom edge; keep the lower body and delivery props fixed rather than translating the whole pet.
- `270` screen-left: yaw the head and snout toward the viewer's left. The snout tip, pupils, and front face edge must read on the screen-left side of the head center and visibly oppose `090` in viewer coordinates.

## Motion budget and interpolation

Each 22.5 degree step advances head yaw or pitch by a similar visual amount. The stable lower-body anchor is shared by all directions. Intermediate poses blend yaw and pitch between neighboring cardinal families; ear and bag follow-through stays smaller than the head movement. The row boundary `157.5 -> 180` and loop boundary `337.5 -> 000` must remain one-step transitions without a scale, baseline, costume, or prop-attachment jump.

## Direction acceptance

Use viewer/screen coordinates. Cardinals must be unmistakable at normal pet size. Diagonals must preserve both intended axes through head, snout, eyes, ears, and restrained torso follow-through. Reject any pose that remains front-facing, rotates the whole sprite, changes the shoe or vest registration, changes the delivery costume or prop connections, or introduces a new facial design.
