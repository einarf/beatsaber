#version 330

#if defined VERTEX_SHADER
in vec3 in_position;

void main() {
    gl_Position = vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER
out vec4 outColor;
uniform sampler2D texture0;

// kernel http://dev.theomader.com/gaussian-kernel-calculator/
const int KERNEL_SIZE = 31;
const int KERNEL_HALF_SIZE = (KERNEL_SIZE - 1) / 2;
const float KERNEL[KERNEL_SIZE] = float[KERNEL_SIZE](
    0.000001, 0.000003, 0.000012, 0.000048, 0.000169, 0.000538, 0.001532, 0.003906, 0.00892, 0.018246, 0.033431, 0.054865,
    0.080656, 0.106209, 0.125279, 0.132368, 0.125279, 0.106209, 0.080656, 0.054865, 0.033431, 0.018246, 0.00892, 0.003906,
    0.001532, 0.000538, 0.000169, 0.000048, 0.000012, 0.000003, 0.000001
);

void main() {
    ivec2 uv = ivec2(gl_FragCoord.xy);
    vec4 col = vec4(0.0);
    for (int i = 0; i < KERNEL_SIZE; i++) {
        col += texelFetch(texture0, uv + ivec2(i - KERNEL_HALF_SIZE, 0), 0) * KERNEL[i];
    }
    outColor = vec4(col.rgb, 1.0);
}

#endif
