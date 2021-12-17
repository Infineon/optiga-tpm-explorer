#ifndef _EHEALTHRPI_H_
#define _EHEALTHRPI_H_

extern void pulsioximeterInit(void); 
extern int getOxygenSaturation(void);
extern int getBPM(void);
extern void clearBPM_SPO2(void);

#endif /* _EHEALTHRPI_H_ */
