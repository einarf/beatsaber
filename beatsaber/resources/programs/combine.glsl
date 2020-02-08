#version 330

#if defined VERTEX_SHADER
in vec3 in_position;
in vec2 in_texcoord_0;
out vec2 uv;

void main() {
    gl_Position = vec4(in_position, 1.0);
    uv = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER
out vec4 outColor;
in vec2 uv;
uniform sampler2D texture0;
uniform sampler2D texture1;

void main() {
    vec4 c1 = texture(texture0, uv);
    vec4 c2 = texture(texture1, uv);
    // outColor = vec4(vec3(length(c1.rgb)), c1.a) + c2 * c1.a;
    outColor = vec4(length(c1.rgb)) + (c2 * (1.0 - c1.a));
}

#endif
