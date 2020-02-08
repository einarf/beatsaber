#version 330

#if defined VERTEX_SHADER

in vec3 in_position;

uniform mat4 m_proj;
uniform mat4 m_model;
uniform mat4 m_cam;

void main() {
    mat4 mv = m_cam * m_model;
    vec4 p = mv * vec4(in_position, 1.0);
    gl_Position = m_proj * p;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform vec4 color;

void main()
{
    fragColor = color;
}

#endif
