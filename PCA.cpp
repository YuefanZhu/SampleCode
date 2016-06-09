#include<stdio.h>
#include<stdlib.h>
#include<math.h>

int _stdcall pca(int n, int T, double *price, double *output_V, double *output_F, double *output_D)
{
	double *eigen, *eigen0, *eigen1, *cov, *cov1, *returns, *V, *F, *D, sum, sum1, sum2, delta;
	int i, j, k, q;
	returns = (double *)calloc(n*(T - 1), sizeof(double));
	//cov is for iteration, cov1 is for recording cov matrix
	cov = (double *)calloc(n*n, sizeof(double));
	cov1 = (double *)calloc(n*n, sizeof(double));
	//eigen is w(0), eigen0 is w(n-1), eigen is w(n)
	eigen = (double *)calloc(n, sizeof(double));
	eigen0 = (double *)calloc(n, sizeof(double));
	eigen1 = (double *)calloc(n, sizeof(double));
	//V is eigenvectors, F is eigenvalues
	V = (double *)calloc(n*10, sizeof(double));
	F = (double *)calloc(10, sizeof(double));
	//D is the difference of cov matrix and V*F*VT
	D = (double *)calloc(n*n, sizeof(double));
	
	//calculate returns
	for (i = 0; i < n; i++){
		for (j = 0; j < T - 1; j++){
			returns[i*(T - 1) + j] = price[i*T + j + 1] / price[i*T + j] - 1;
		}
	}
	T = T - 1;

	//calculate cov matrix
	for (i = 0; i < n; i++){
		for (j = 0; j < n; j++){
			sum = 0;
			sum1 = 0;
			sum2 = 0;
			for (k = 0; k < T; k++){
				sum1 += returns[i*T + k];
				sum2 += returns[j*T + k];
			}
			for (k = 0; k < T; k++){
				sum += (returns[i*T + k] - sum1 / T) * (returns[j*T + k] - sum2 / T);
			}
			cov[i*n + j] = sum / (T - 1);
			//Important! cant use cov1=cov; when cov changes, cov1 changes too because they are with the same address
			cov1[i*n + j] = cov[i*n + j];
		}
	}
	

	//Implement power method to find eigenvectors and eigenvalues
	for (i = 0; i < n; i++){
		eigen[i] = 1/sqrt(double(n));
	}
	//want 10 components
	for (q = 0; q < 10; q++){
		delta = 1;
		for (i = 0; i < n; i++){
			eigen0[i] = eigen[i];
		}
		while (delta > 0.00000000000000000001){
			for (i = 0; i < n; i++){
				eigen1[i] = 0;
				for (j = 0; j < n; j++){
					eigen1[i] += cov[i*n + j] * eigen0[j];
				}
			}
			//standardize eigen1
			sum = 0;
			for (i = 0; i < n; i++){
				sum += eigen1[i] * eigen1[i];
			}
			for (i = 0; i < n; i++){
				eigen1[i] = eigen1[i] / sqrt(sum);
			}
			//delta=sum of the square of difference between eigen1 and eigen0
			delta = 0;
			for (i = 0; i < n; i++){
				delta += (eigen0[i] - eigen1[i])*(eigen0[i] - eigen1[i]);
			}
			for (i = 0; i < n; i++){
				eigen0[i] = eigen1[i];
			}
		}
		//record eigenvector in V
		for (i = 0; i < n; i++){
			V[i * 10 + q] = eigen1[i];
		}
		//estimate lambda and record it in F
		sum = 0;
		for (i = 0; i < n; i++){
			eigen1[i] = 0;
			for (j = 0; j < n; j++){
				eigen1[i] += cov[i*n + j] * eigen0[j];
			}
			sum += eigen1[i] / eigen0[i];
		}
		F[q] = sum / n;
		//find cov' and eigen0' for next loop
		sum = 0;
		for (i = 0; i < n; i++){
			sum += eigen[i] * eigen0[i];
		}
		for (i = 0; i < n; i++){
			eigen[i] = eigen[i] - sum*eigen0[i];
		}
		for (i = 0; i < n; i++){
			for (j = 0; j < n; j++){
				cov[i*n + j] = cov[i*n + j] - F[q] * eigen0[i] * eigen0[j];
			}
		}
	}
	//estimate D
	for (i = 0; i < n; i++){
		for (j = 0; j < n; j++){
			sum = 0;
			for (k = 0; k < 10; k++){
				sum += F[k] * V[i * 10 + k] * V[j * 10 + k];
			}
			D[i*n + j] = cov1[i*n + j] - sum;
		}
	}
	//output
	for (i = 0; i < n; i++){
		for (j = 0; j < 10; j++){
			output_V[i*10+j] = V[i * 10 + j];
		}
	}
	for (i = 0; i < 10; i++){
		output_F[i] = F[i];
	}
	for (i = 0; i < n; i++){
		for (j = 0; j < n; j++){
			output_D[i*n + j] = D[i*n + j];
		}
	}
	//Then free memory in VBA
	return 1;
}


