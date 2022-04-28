from dataclasses import dataclass
import numpy as np

from utils.geometry import Vec2, Vec3
from utils.sig import metsig

from objects.element import Element, ElementSpecification, ShapeSpec
from shader import ShaderDB
from transformation_matrix import Transform


@dataclass(init=False)
class Garbage(Element):
    rotation_speed: float = 0.01

    @metsig(Element.__init__)
    def __init__(self, *args, **kwargs):
        garbage_color: Vec3 = Vec3(119, 119, 119) / 255

        kwargs['specs'] = ElementSpecification(
            initial_transform=Transform(
                translation=Vec3(0, 0, 0),
                rotation=Vec3(0, 0, 0),
                scale=Vec3(1, 1, 1),
            ),
            shape_specs=[
                ShapeSpec(
                    vertices=np.array([
                        *(-0.025, -0.040, +0.0), *(garbage_color),
                        *( 0.025, -0.040, +0.0), *(garbage_color),
                        *(-0.025,  0.040, +0.0), *(garbage_color),

                        *(-0.025,  0.040, +0.0), *(garbage_color),
                        *( 0.025, -0.040, +0.0), *(garbage_color),
                        *( 0.025,  0.040, +0.0), *(garbage_color),
                    ], dtype=np.float32),
                    shader=ShaderDB.get_instance().get_shader('colored'),
                )
            ]
        )

        super().__init__(*args, **kwargs)

    def _get_bounding_box_vertices(self) -> np.ndarray:
        return np.array([
            [*(-0.025, -0.040, +0.0)],
            [*( 0.025, -0.040, +0.0)],
            [*(-0.025,  0.040, +0.0)],
            [*(-0.025,  0.040, +0.0)],
        ])

    def _physics_update(self, delta_time: float):
        self.rotate(self.rotation_speed)
        super()._physics_update(delta_time)
