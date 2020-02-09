#version 330

#if defined VERTEX_SHADER

in vec3 in_position;

uniform mat4 m_proj;
uniform mat4 m_cam;

void main() {
    gl_Position = m_proj * m_cam * vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform vec4 color;

void main()
{
    fragColor = color;
}

#endif
