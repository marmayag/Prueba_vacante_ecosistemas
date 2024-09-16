SELECT commerce.commerce_id,
    commerce.commerce_nit,
    commerce.commerce_name,
    commerce.commerce_email,
    strftime('%Y%m', apicall.date_api_call) AS formatted_date,
    -- Contar los 'Successful'
    SUM(
        CASE
            WHEN apicall.ask_status = 'Successful' THEN 1
            ELSE 0
        END
    ) AS successful_count,
    -- Contar los 'Unsuccessful'
    SUM(
        CASE
            WHEN apicall.ask_status = 'Unsuccessful' THEN 1
            ELSE 0
        END
    ) AS unsuccessful_count
FROM commerce AS commerce
    LEFT JOIN apicall AS apicall ON commerce.commerce_id = apicall.commerce_id
WHERE apicall.date_api_call BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
    AND commerce.commerce_status = '{commerce_status}'
GROUP BY commerce.commerce_id,
    strftime('%Y%m', apicall.date_api_call);