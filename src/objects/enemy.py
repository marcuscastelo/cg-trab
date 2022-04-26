from utils.logger import LOGGER
from utils.sig import metsig
from objects.element import Element
from objects.projectile import Projectile

from OpenGL import GL as gl

class Enemy(Element):
    @metsig(Element.__init__)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dying = False
        pass

    def _init_vertices(self):
        # self._render_primitive = gl.GL_LINE_STRIP
        self._vertices = [
            *(-0.1, -0.1, 0.0),
            *(0.1, -0.1, 0.0),
            *(0.1, 0.1, 0.0),

            *(-0.1, -0.1, 0.0),
            *(-0.1, 0.1, 0.0),
            *(0.1, 0.1, 0.0),
        ]
    
    def _physics_update(self, delta_time: float):
        min_x, min_y, max_x, max_y = Element.get_bounding_box(self)
        projectiles = ( element for element in self.world.elements if isinstance(element, Projectile) )

        for projectile in projectiles:
            if projectile.is_particle:
                continue
            
            if projectile.x < min_x or projectile.x > max_x:
                continue
            if projectile.y < min_y or projectile.y > max_y:
                continue

            LOGGER.log_debug(f'Enemy(id={id(self)}) hit by projectile(id={id(projectile)})')
            self.die()
            projectile.destroy()

        pass

    def _render(self):
        if self.dying:
            self.transform.scale *= 0.9
            if self.transform.scale.x < 0.1:
                self.destroy()
                return

        return super()._render()

    def die(self):
        self.dying = True

    def destroy(self):
        return super().destroy()