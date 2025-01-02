(define (reduce f init lst)
  (if (null? lst)
      init
      (reduce f (f init (car lst)) (cdr lst))))

(define (suma2 a b) (+ a b))
(define (mult2 a b) (* a b))

(define datos '(1 2 3 4 5))

(define (main)
  (display (reduce suma2 0 datos))
  (newline)
  (display (reduce mult2 1 datos))
  (newline))