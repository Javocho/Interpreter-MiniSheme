(define (concatena l1 l2)
  (if (null? l1)
      l2
      (cons (car l1) (concatena (cdr l1) l2))))

(define (main)
  (display (concatena '(1 2) '(3 4 5)))
  (newline)
  (display (concatena '() '(7 8)))
  (newline))