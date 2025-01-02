(define (f x)
  (cond
    ((< x 0) "neg")
    ((= x 0) "zero")
    (#t "pos")))

(define (main)
  (display (f -3))
  (newline)
  (display (f 0))
  (newline)
  (display (f 10))
  (newline))