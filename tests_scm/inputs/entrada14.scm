(define (aplica-varias-veces f x n)
  (if (= n 0)
      x
      (aplica-varias-veces f (f x) (- n 1))))

(define (inc x) (+ x 1))

(define (main)
  (display (aplica-varias-veces inc 5 0))
  (newline)
  (display (aplica-varias-veces inc 5 3))
  (newline))