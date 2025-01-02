(define (sumar-hasta-cero acum)
  (let ((x (read)))
    (if (= x 0)
        acum
        (sumar-hasta-cero (+ acum x)))))

(define (main)
  (display "Introduce numeros, 0 para terminar:")
  (newline)
  (display (sumar-hasta-cero 0))
  (newline))