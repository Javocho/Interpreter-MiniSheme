(define (prod-list lst)
  (if (null? lst)
      1
      (* (car lst) (prod-list (cdr lst)))))

(define (main)
  (display (prod-list '(2 3 4)))
  (newline)
  (display (prod-list '()))
  (newline))