(define datos '((1 2) (3 4 5) () (6 7)))

(define (main)
  (display (car datos))
  (newline)
  (display (cdr datos))
  (newline)
  (display (car (car datos)))
  (newline))