-- Partie 1
SELECT	t1.DATE AS DATE, SUM(t1.PROD_PRICE*t1.PROD_QTY) AS VENTES
FROM TRANSACTIONS t1
WHERE t1.DATE BETWEEN DATE(2019,01,01) AND DATE(2019,12,31)
GROUP BY t1.DATE
ORDER BY t1.DATE ASC;