#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <stdint.h>

#include <wiringPi.h>

#define	G7	24
#define	F6	23
#define	E5	5
#define	D4	4
#define	C3	3
#define	B2	2
#define	A1	0
#define	IRQ	25

uint16_t	SPO2;
uint16_t	BPM;

//!******************************************************************************
//! Converts from 7 segments to number.
//!  --A--
//! |     |
//! C     B
//! |     |
//!  --D--
//! |     |
//! F     E
//! |     |
//!  --G--
//!******************************************************************************
uint8_t segToNumber(uint8_t A, uint8_t B, uint8_t C, uint8_t D, uint8_t E, uint8_t F, uint8_t G )
{
	if ((A == 1) && (B == 1) && (C == 1) && (D == 0) && (E == 1) && (F == 1) && (G == 1)) {
		return 0;
	} else if ((A == 0) && (B == 1) && (C == 0) && (D == 0) && (E == 1) && (F == 0) && (G == 0)) {
		return 1;
	} else if ((A == 1) && (B == 1) && (C == 0) && (D == 1) && (E == 0) && (F == 1) && (G == 1)) {
		return 2;
	} else if ((A == 1) && (B == 1) && (C == 0) && (D == 1) && (E == 1) && (F == 0) && (G == 1)) {
		return 3;
	} else if ((A == 0) && (B == 1) && (C == 1) && (D == 1) && (E == 1) && (F == 0) && (G == 0)) {
		return 4;
	} else if ((A == 1) && (B == 0) && (C == 1) && (D == 1) && (E == 1) && (F == 0) && (G == 1)) {
		return 5;
	} else if ((A == 1) && (B == 0) && (C == 1) && (D == 1) && (E == 1) && (F == 1) && (G == 1)) {
		return 6;
	} else if ((A == 1) && (B == 1) && (C == 0) && (D == 0) && (E == 1) && (F == 0) && (G == 0)) {
		return 7;
	} else if ((A == 1) && (B == 1) && (C == 1) && (D == 1) && (E == 1) && (F == 1) && (G == 1)) {
		return 8;
	} else if ((A == 1) && (B == 1) && (C == 1) && (D == 1) && (E == 1) && (F == 0) && (G == 1)) {
		return 9;
	} else if ((A == 0) && (B == 0) && (C == 0) && (D == 1) && (E == 0) && (F == 0) && (G == 0)) {
		return '-'; // sampling
	} else if ((A == 0) && (B == 0) && (C == 0) && (D == 0) && (E == 0) && (F == 0) && (G == 0)) {
		return ' '; // No digit (Space)
	} else  {
		//printf("%x %x %x %x %x %x %x \n", A,B,C,D,E,F,G);
		return 0xFF; // unknown (EOF)
	}
}

//!******************************************************************************
//!		Name:	pulsioximeterIRQ()					*
//!		Description: Interrupt Rountine.				*
//!		Param : void							*
//!		Returns: void							*
//!******************************************************************************
void pulsioximeterIRQ (void)
{
	static uint8_t cnt=0;
	uint8_t digito[10];

	uint8_t A;
	uint8_t B;
	uint8_t C;
	uint8_t D;
	uint8_t E;
	uint8_t F;
	uint8_t G;

	int i;

	if (cnt == 50) { //Get only of one 50 measures to reduce the latency
		cnt=0;
		A=B=C=D=E=F=G=0;

		delayMicroseconds(70); // short delay before sampling
		i=0;
		do {
			A = digitalRead(A1);
			B = digitalRead(B2);
			C = digitalRead(C3);
			D = digitalRead(D4);
			E = digitalRead(E5);
			F = digitalRead(F6);
			G = digitalRead(G7);

			digito[i] = segToNumber(A, B, C ,D ,E, F,G);

			if(digito[i] != ' ')
				i++;

			delayMicroseconds(380); //sample freq in microseconds
		}while (digito[i-1] != 0xFF);

		if(digito[0] != '-')
		{
			if((digito[2] <= 2) && ((i-1)>=4 ))
			{
				BPM = 100 * digito[2] + 10 * digito[1] + digito[0];
				SPO2 = 10 * digito[4] + digito[3];
			} else {
				BPM = 10 * digito[1] + digito[0];
				SPO2  = 10 * digito[3] + digito[2];
			}
		} else {
			BPM = digito[0];
			SPO2 = digito[0];
		}
	} else {
		cnt++;
	}
}

//!******************************************************************************
//!		Name:	getOxygenSaturation()
//!		Description: Returns the oxygen saturation in blood in percent.
//!		Param : void
//!		Returns: int with the oxygen saturation value
//!******************************************************************************
int getOxygenSaturation(void)
{
	return SPO2;
}

//!******************************************************************************
//!		Name:	getBPM()														*
//!		Description: Returns the heart beats per minute.						*
//!		Param : void															*
//!		Returns: int with the beats per minute									*
//!******************************************************************************
int getBPM(void)
{
	return BPM;
}

//!******************************************************************************
//!		Name:	ClearBPM_SPO2()													*
//!		Description: Set the BPM ans SPO2 to zero					        	*
//!		Param : void															*
//!		Returns: void															*
//!******************************************************************************
void clearBPM_SPO2(void)
{
	BPM=0;
	SPO2=0;
}


//!******************************************************************************
//!		Name:	pulsioximeterInit()												*
//!		Description: Initializes the pulsioximeter sensor.						*
//!		Param : void															*
//!		Returns: void															*
//!******************************************************************************

void pulsioximeterInit(void) 
{
	SPO2 = 0;
	BPM = 0;
	
	// Configuring digital pins like INPUTS
	//wiringPiSetup();
	
	pinMode(IRQ, INPUT);	// IRQ Signal Flags 
	pinMode(G7, INPUT); 	// G7
	pinMode(F6, INPUT); 	// F6
	pinMode(E5, INPUT);  	// E5
	pinMode(D4, INPUT);  	// D4
	pinMode(C3, INPUT);  	// C3
	pinMode(B2, INPUT);  	// B2
	pinMode(A1, INPUT);  	// A1 

	// Set IRQ for start of frame
	if (wiringPiISR (IRQ, INT_EDGE_FALLING, &pulsioximeterIRQ) < 0)
	{
		fprintf (stderr, "Unable to setup ISR: %s\n", strerror (errno)) ;
		exit(1);
	}
}

