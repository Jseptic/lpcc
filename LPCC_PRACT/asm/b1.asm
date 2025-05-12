START 150
    READ D
    READ E
LOOP	 MOVER AREG, D  
	 MOVER BREG, E  
    COMP BREG, =’20’ 
	 BC GT, LOOP
BACK SUB AREG, E
            COMP AREG, =’50’
	 BC  LT, BACK 
    STOP
D	 DS	1
E	 DS	1
	 END
