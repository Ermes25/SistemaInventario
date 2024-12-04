USE sistemainventario;

INSERT INTO productos (nombre_producto, categoria, fecha_vencimiento, cantidad, precio) VALUES
('Paracetamol 500mg', 'Medicamento', '2025-06-30', 150, 75),
('Ibuprofeno 400mg', 'Medicamento', '2026-04-15', 200, 85),
('Loratadina 10mg', 'Medicamento', '2026-09-01', 180, 95),
('Omeprazol 20mg', 'Medicamento', '2025-12-20', 120, 110),
('Amoxicilina 500mg', 'Antibiótico', '2025-08-30', 100, 120),
('Ciprofloxacino 500mg', 'Antibiótico', '2025-07-20', 80, 150),
('Metformina 850mg', 'Control Diabetes', '2026-01-10', 90, 065),
('Losartán 50mg', 'Hipertensión', '2026-03-25', 110, 70),
('Simvastatina 20mg', 'Colesterol', '2025-11-10', 100, 80),
('Insulina NPH', 'Control Diabetes', '2025-09-30', 50, 12),
('Multivitamínico Adulto', 'Suplemento', '2026-05-01', 150, 2.50),
('Vitamina C 500mg', 'Suplemento', '2025-07-15', 180, 50),
('Calcio + Vitamina D', 'Suplemento', '2026-02-28', 100, 3),
('Alcohol Gel 70%', 'Antiséptico', '2025-06-30', 300, 175),
('Yodopovidona 10%', 'Antiséptico', '2025-10-20', 120, 210),
('Curitas Adhesivas', 'Primeros Auxilios', '2027-12-31', 250, 10),
('Gasa Estéril', 'Primeros Auxilios', '2027-12-31', 150, 25),
('Clotrimazol Crema', 'Antimicótico', '2025-08-15', 90, 150),
('Jarabe para la Tos', 'Medicamento', '2025-07-30', 80, 180),
('Antigripal Tabletas', 'Medicamento', '2025-12-01', 100, 95),
('Sales de Rehidratación', 'Rehidratante', '2026-06-15', 120, 40),
('Suero Oral', 'Rehidratante', '2025-12-20', 150, 85),
('Anticonceptivo Oral', 'Control Familiar', '2026-05-01', 100, 200),
('Anticonceptivo Inyectable', 'Control Familiar', '2026-10-10', 50, 30),
('Crema Analgésica', 'Analgésico', '2025-11-01', 70, 200),
('Jeringas Desechables', 'Equipo Médico', '2028-01-01', 300, 25),
('Termómetro Digital', 'Equipo Médico', '2030-12-31', 50, 50),
('Preservativos', 'Control Familiar', '2027-06-01', 200, 75),
('Desinfectante Líquido', 'Limpieza', '2025-09-30', 100, 250),
('Guantes Desechables', 'Equipo Médico', '2027-12-31', 200, 15);


INSERT INTO proveedores (nombre_proveedor, numero_proveedor, email) VALUES
('Casa Teran', '22285000', NULL),
('Farcosa', '22699486', 'farcosa.com.ni'),
('Didelsa', '22489200', 'didelsa.com.ni'),
('Generipharma', '22493765', 'generifar.com.ni'),
('Droguería Rocha', '84150747', 'drogueriarocha.com');

