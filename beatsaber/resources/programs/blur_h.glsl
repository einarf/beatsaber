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

// kernel http://dev.theomader.com/gaussian-kernel-calculator/
const int NUM_LAYERS = 10;
const int KERNEL_SIZE = 5;
const int KERNEL_HALF_SIZE = (KERNEL_SIZE - 1) / 2;
const float KERNEL[KERNEL_SIZE] = float[KERNEL_SIZE](0.06137, 0.24477, 0.38774, 0.24477, 0.06137);

void main() {
    vec4 col = vec4(0.0);
    for (int layer = 0; layer < NUM_LAYERS; layer++) {
        vec2 uv_step = uv / textureSize(texture0, layer).xy;
        for (int i = 0; i < KERNEL_SIZE; i++) {
            col += texture(texture0, uv + vec2(uv_step.x * (i - KERNEL_HALF_SIZE)), layer) * KERNEL[i] * 2.0;
        }
    }
    outColor = vec4(col.rgb, 1.0) / KERNEL_SIZE;
}

#endif
