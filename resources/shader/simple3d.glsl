#version 460



#ifdef VERTEX_SHADER

uniform mat4 mvp;
in vec3 in_position;
in vec2 in_texcoord_0;
in vec3 in_normal;

in vec3 in_offset;

out vec2 uv;
out vec3 N;

void main(){
    gl_Position = mvp*vec4(in_position+in_offset, 1.0);
    uv = in_texcoord_0;
    N = normalize(in_normal);
}

#elif FRAGMENT_SHADER

in vec2 uv;
in vec3 N;
layout(location=0) out vec4 fragColor;

void main(){
    fragColor = vec4(N, 0.0);
}

#endif

