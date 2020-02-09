#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;

uniform mat4 m_proj;
uniform mat4 m_cam;
uniform float rotation;

out vec3 normal;

const float PI = 3.14159265358;

void main() {
    // Manually create rotation matrix and offset origin
    float r = rotation + sin(gl_InstanceID * (rotation / 4.0));
    mat4 rot = mat4(
        cos(r), -sin(r), 0.0, 0.0,
        sin(r), cos(r), 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 3.0, 0.0, 1.0
    );
    mat4 trans = mat4(
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, -3.0, 0, 1.0
    );

    mat4 mv = m_cam * (rot * trans);
    vec4 p = mv * vec4(in_position + vec3(0.0, 0.0, -10.0 * gl_InstanceID) , 1.0);
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
