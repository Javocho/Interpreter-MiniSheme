(define (multiplicar a b) (* a b))

(define global 100)

(define (main)
  (let ((a 50) (b 2))
    (display (multiplicar global b))
    (newline)))