CREATE OR REPLACE FUNCTION insert_historial()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO historial (id_reserva, id_usuario, id_laboratorio)
    VALUES (NEW.id_reserva, NEW.id_usuario, NEW.id_laboratorio);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER after_reserva_insert
AFTER INSERT ON reserva
FOR EACH ROW
EXECUTE FUNCTION insert_historial();
