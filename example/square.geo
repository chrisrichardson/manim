SetFactory("OpenCASCADE");

Mesh.Algorithm = 6;
Mesh.CharacteristicLengthMin = 1.0;
Mesh.CharacteristicLengthMax = 1.0;

Rectangle(1) = {-3.0, -3.0, 0.0, 6.0, 6.0};
