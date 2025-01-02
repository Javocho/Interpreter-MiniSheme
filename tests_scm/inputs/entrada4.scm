(define (clasifica n)
  (cond
    ((< n 0) "negativo")
    ((= n 0) "cero")
    ((> n 0) "positivo")))

(define (main)
  (display (clasifica -5)) ;arg negatiu (al començament m'ho detectava com 2 args)
  (newline)
  (display (clasifica 0))
  (newline)
  (display (clasifica 10))
  (newline))