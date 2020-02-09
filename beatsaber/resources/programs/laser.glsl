#version 330

#if defined VERTEX_SHADER

in vec3 in_position;

uniform mat4 m_proj;
uniform mat4 m_cam;
uniform float rotation;
uniform float time;

void main() {
    float r = rotation * (gl_InstanceID + 1) / 4.0 + sin(time) / 3.0;
    mat4 rot = mat4(
        cos(r), -sin(r), 0.0, 0.0,
        sin(r), cos(r), 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0
    );

    mat4 mv = m_cam * rot;
    vec4 p = mv * vec4(in_position + vec3(0.0, 20.0, -40 + -5.0 * gl_InstanceID), 1.0);
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
