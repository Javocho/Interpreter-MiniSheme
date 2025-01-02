(define (fact n)
  (if (<= n 1)
      1
      (* n (fact (- n 1)))))

(define (map f lst)
  (cond ((null? lst) '())
        (else (cons (f (car lst)) (map f (cdr lst))))))

(define (main)
  (display (map fact '(1 2 3 4)))
  (newline))