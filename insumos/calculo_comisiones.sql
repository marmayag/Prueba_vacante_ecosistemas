WITH t1 AS (
    -- Cruces con descuentos y comisiones
    SELECT consolidado.commerce_nit,
        consolidado.commerce_name,
        consolidado.commerce_email,
        consolidado.formatted_date,
        consolidado.successful_count,
        consolidado.unsuccessful_count,
        comisiones.costo_comision,
        comisiones.porcentaje_iva,
        descuentos.porcentaje_descuento,
        CASE
            WHEN consolidado.successful_count BETWEEN comisiones.lim_inf_successful AND comisiones.lim_sup_successful THEN 'yes'
            ELSE 'no'
        END AS marca_successful,
        CASE
            WHEN consolidado.unsuccessful_count BETWEEN descuentos.lim_inf_unsuccessful AND descuentos.lim_sup_unsuccessful THEN 'yes'
            ELSE 'no'
        END AS marca_unsuccessful
    FROM consolidado_sin_comisiones AS consolidado
        LEFT JOIN comisiones AS comisiones ON consolidado.commerce_name = comisiones.commerce_name
        LEFT JOIN descuentos AS descuentos ON consolidado.commerce_name = descuentos.commerce_name
) -- Solo me traigo lo que cumple con y sin descuentos
SELECT formatted_date AS fecha_mes,
    commerce_name AS nombre,
    commerce_nit AS nit,
    (costo_comision * successful_count) * (
        1 - (
            CASE
                WHEN porcentaje_descuento IS NULL THEN 0
                ELSE porcentaje_descuento
            END
        )
    ) AS valor_comision,
    (costo_comision * successful_count) * (
        1 - (
            CASE
                WHEN porcentaje_descuento IS NULL THEN 0
                ELSE porcentaje_descuento
            END
        )
    ) * porcentaje_iva AS valor_iva,
    (costo_comision * successful_count) * (
        1 - (
            CASE
                WHEN porcentaje_descuento IS NULL THEN 0
                ELSE porcentaje_descuento
            END
        )
    ) * (1 + porcentaje_iva) AS valor_total,
    commerce_email AS correo
FROM t1
WHERE (
        porcentaje_descuento IS NULL
        AND marca_successful = "yes"
    )
    OR (
        marca_successful = "yes"
        AND marca_unsuccessful = "yes"
    );