(define (longitud lst)
  (if (null? lst)
      0
      (+ 1 (longitud (cdr lst)))))

(define datos '(1 2 3 4 5))

(define (main)
  (display (longitud datos))
  (newline)
  (display (longitud '()))
  (newline))