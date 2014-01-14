function getShader(gl, id) {
	//to be implemented
}

function setMatrixUniforms() {
	gl.uniformMatrix4fv(ShaderProgram.pMatrixUniform,false,pMatrix);
	gl.uniformMatrix4fv(ShaderProgram.mvMatrixUniform,false,mvMatrix);
}