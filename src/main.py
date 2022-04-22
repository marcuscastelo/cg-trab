from dataclasses import dataclass
import math
from threading import Thread
from typing import Callable

import glfw
import OpenGL.GL as gl

from threading import Thread

from utils.logger import LOGGER
from utils.geometry import Vec2Int

from constants import WINDOW_SIZE
from app_state import STATE
from gui import AppGui

import numpy as np

import keyboard

def create_window():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    window = glfw.create_window(*WINDOW_SIZE, "Simple Window", monitor=None, share=None)
    glfw.make_context_current(window)
    glfw.show_window(window)
    return window


def gen_cubes_pos():
    CENTER = np.array([0.0, 0.0, 0.0])
    MINCUBE_LENGTH = 1

    x, y, z = -MINCUBE_LENGTH, -MINCUBE_LENGTH, -MINCUBE_LENGTH

    while True:
        yield np.array([x, y, z])
        x += MINCUBE_LENGTH
        if x > MINCUBE_LENGTH:
            x = -MINCUBE_LENGTH
            y += MINCUBE_LENGTH
        if y > MINCUBE_LENGTH:
            y = -MINCUBE_LENGTH
            z += MINCUBE_LENGTH
        if z > MINCUBE_LENGTH:
            z = -MINCUBE_LENGTH
            x = -MINCUBE_LENGTH

def gen_face_vertices():

    for cube_pos in gen_cubes_pos():
        pass

    pass

'''
(2, 2, -2)
(0, 2, -2)
(2, 2, 0)
(0, 2, 0)

(2, 0, 0)
(2, 0, -2)
(2, 2, 0)
(2, 2, -2)

(0, 0, -2)
(2, 0, -2)
(2, 2, -2)
(0, 2, -2)
'''


@dataclass
class Vec3:
    x: float
    y: float
    z: float = 0.0

def gen_face_vertices(face_pos: Vec3) -> np.ndarray:

    return np.array([
        # FRONTAL FACE (Z does not change)
        -0.33+face_pos.x     , -0.33+face_pos.y   , -0.33+face_pos.z,
        +0.33+face_pos.x     , -0.33+face_pos.y   , -0.33+face_pos.z,
        +0.33+face_pos.x     , +0.33+face_pos.y   , -0.33+face_pos.z,

        -0.33+face_pos.x     , -0.33+face_pos.y   , -0.33+face_pos.z,
        +0.33+face_pos.x     , +0.33+face_pos.y   , -0.33+face_pos.z,
        -0.33+face_pos.x     , +0.33+face_pos.y   , -0.33+face_pos.z,

        # SIDE FACES (X does not change)
        -0.33+face_pos.x     , -0.33+face_pos.y   , -0.33+face_pos.z,
        -0.33+face_pos.x     , -0.33+face_pos.y   , +0.33+face_pos.z,
        -0.33+face_pos.x     , +0.33+face_pos.y   , +0.33+face_pos.z,

        -0.33+face_pos.x     , -0.33+face_pos.y   , -0.33+face_pos.z,
        -0.33+face_pos.x     , +0.33+face_pos.y   , +0.33+face_pos.z,
        -0.33+face_pos.x     , +0.33+face_pos.y   , -0.33+face_pos.z,

        # TOP FACES (Y does not change)
        -0.33+face_pos.x     , +0.33+face_pos.y   , -0.33+face_pos.z,
        +0.33+face_pos.x     , +0.33+face_pos.y   , -0.33+face_pos.z,
        +0.33+face_pos.x     , +0.33+face_pos.y   , +0.33+face_pos.z,

        -0.33+face_pos.x     , +0.33+face_pos.y   , -0.33+face_pos.z,
        +0.33+face_pos.x     , +0.33+face_pos.y   , +0.33+face_pos.z,
        -0.33+face_pos.x     , +0.33+face_pos.y   , +0.33+face_pos.z,


    ], dtype=np.float32)

vertices = [
    *gen_face_vertices(Vec3(0.0,0.0,0.0)),
    # *gen_face_vertices(Vec3(0.66,0.0,0.0)),
    # *gen_face_vertices(Vec3(-0.66,0.0,0.0)),
]

def render_rubik_cube():
    pass

def glfw_thread():
    window = create_window()

    with open('shaders/vertex_shader.vert', 'r') as f:
        vertex_shader_source = f.read()

    with open('shaders/fragment_shader.frag', 'r') as f:
        fragment_shader_source = f.read()

    program = gl.glCreateProgram()
    vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    fragment_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

    gl.glShaderSource(vertex_shader, vertex_shader_source)
    gl.glShaderSource(fragment_shader, fragment_shader_source)

    gl.glCompileShader(vertex_shader)
    
    gl.glCompileShader(fragment_shader)

    gl.glAttachShader(program, vertex_shader)
    gl.glAttachShader(program, fragment_shader)

    gl.glLinkProgram(program)

    gl.glUseProgram(program)
    # return

    vao = gl.glGenVertexArrays(1)
    vbo = gl.glGenBuffers(1)

    gl.glBindVertexArray(vao)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)

    # vertices = [
    #     0.0,  0.866025403784-0.5+0.183012701892, 0.0,
    #     0.5, -0.5+0.183012701892, 0.0,
    #     -0.5, -0.5+0.183012701892, 0.0
    # ]


    # Set the vertex buffer data
    gl.glBufferData(gl.GL_ARRAY_BUFFER, len(vertices)*4, (gl.GLfloat * len(vertices))(*vertices), gl.GL_STATIC_DRAW)

    gl.glEnableVertexAttribArray(0)
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

    gl.glEnableVertexAttribArray(1)
    gl.glVertexAttribPointer(1, 1, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
    mvp_loc = gl.glGetUniformLocation(program, 'mvp')



    # Use a FBO instead of the default framebuffer
    fbo = gl.glGenFramebuffers(1)
    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, fbo)

    # Create a texture to render to
    texture = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, *WINDOW_SIZE, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, None)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)

    # Attach the texture to the FBO
    gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D, texture, 0)

    STATE.texture = texture

    while not glfw.window_should_close(window) and not STATE.closing:
        glfw.poll_events()

        def render():
            gl.glUniformMatrix4fv(mvp_loc, 1, gl.GL_FALSE, STATE.mvp_manager.mvp)

            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            gl.glClearColor(1.0, 1.0, 1.0, 1.0)

            gl.glBindVertexArray(vao)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)

            # Draw the triangle
            gl.glColor3f(1.0, 1.0, 0.0)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, len(vertices))


        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, fbo)
        render()

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        render()

        glfw.swap_buffers(glfw.get_current_context())
    
    LOGGER.log_info("GLFW thread is closing", 'glfw_thread')
    STATE.closing = True

def register_keyboard_controls():
    TRANSLATION_STEP = 0.04
    ROTATION_STEP = 2*math.pi/360 * 5
    SCALE_STEP = 0.2

    def callback_gen(step: float, callback: Callable[[float], None]):
        # if shift is pressed, the step is increased
        def callback_wrapper(*_args):
            print(f"shift is pressed: {keyboard.is_pressed('shift')}")
            if keyboard.is_pressed('shift'):
                callback(step * 2)
            elif keyboard.is_pressed('ctrl'):
                callback(step / 2)
            else:
                callback(step)
        
        return callback_wrapper


    keyboard.on_press_key('w', callback_gen(TRANSLATION_STEP, lambda step: STATE.mvp_manager.translate(0.0, step)))
    keyboard.on_press_key('s', callback_gen(TRANSLATION_STEP, lambda step: STATE.mvp_manager.translate(0.0, -step)))
    keyboard.on_press_key('a', callback_gen(TRANSLATION_STEP, lambda step: STATE.mvp_manager.translate(-step, 0.0)))
    keyboard.on_press_key('d', callback_gen(TRANSLATION_STEP, lambda step: STATE.mvp_manager.translate(step, 0.0)))
    keyboard.on_press_key('q', callback_gen(ROTATION_STEP, lambda step: STATE.mvp_manager.rotate(step)))
    keyboard.on_press_key('e', callback_gen(ROTATION_STEP, lambda step: STATE.mvp_manager.rotate(-step)))
    keyboard.on_press_key('z', callback_gen(SCALE_STEP, lambda step: STATE.mvp_manager.zoom(step)))
    keyboard.on_press_key('x', callback_gen(SCALE_STEP, lambda step: STATE.mvp_manager.zoom(-step)))



def main():
    register_keyboard_controls()

    LOGGER.log_info("Starting app", 'main')

    LOGGER.log_trace("Init Glfw", 'main')
    glfw.init()
    
    LOGGER.log_trace("Init GUI", 'main')
    gui = AppGui()

    LOGGER.log_trace("Start GLFW thread", 'main')
    t = Thread(target=glfw_thread)
    t.start()

    # LOGGER.log_trace("Start GUI", 'main')
    # gui.run()

    LOGGER.log_info("GUI Has been closed, waiting for GLFW to close...", 'main')
    t.join()
    LOGGER.log_info("GLFW thread has been closed", 'main')

    LOGGER.log_trace("Terminating Glfw", 'main')
    glfw.terminate()
    LOGGER.log_info("App has been closed gracefully", 'main')

if __name__ == "__main__":
    main()