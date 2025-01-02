(define (filter f lista)
  (cond
    ((null? lista) '())
    ((f (car lista)) (cons (car lista) (filter f (cdr lista))))
    (else (filter f (cdr lista)))))

(define (pos? x) (> x 0))

(define (main)
  (display (filter pos? '()))
  (newline)
  (display (filter pos? '(-1 0 1 2 -5 3)))
  (newline))