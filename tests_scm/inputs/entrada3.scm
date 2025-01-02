(define (compara a b)
  (if (> a b)
      "a es mayor"
      "b es mayor o igual"))

(define (main)
  (display (compara 10 5))
  (newline)
  (display (compara 2 7))
  (newline)
  (display (compara 5 5))
  (newline))