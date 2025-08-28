(defun gps-line ()
  (interactive)
  (let ((start (point-min))
	(n (line-number-at-pos)))
    (save-excursion
    (save-restriction
      (widen)
      (beginning-of-buffer)
      (let ((cnt 0))
	(while (search-forward "\n" nil t)
	  (setq cnt (+ cnt 1)))
	(message "Line %d/%d"
		 (+ n (line-number-at-pos start) -1) cnt
		 ))))))
