import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
# Procrustes rotation credit to Internet
def procrustes(X, Y, scaling=True, reflection='best'):
    """
    A port of MATLAB's `procrustes` function to Numpy.

    Procrustes analysis determines a linear transformation (translation,
    reflection, orthogonal rotation and scaling) of the points in Y to best
    conform them to the points in matrix X, using the sum of squared errors
    as the goodness of fit criterion.

        d, Z, [tform] = procrustes(X, Y)

    Inputs:
    ------------
    X, Y    
        matrices of target and input coordinates. they must have equal
        numbers of  points (rows), but Y may have fewer dimensions
        (columns) than X.

    scaling 
        if False, the scaling component of the transformation is forced
        to 1

    reflection
        if 'best' (default), the transformation solution may or may not
        include a reflection component, depending on which fits the data
        best. setting reflection to True or False forces a solution with
        reflection or no reflection respectively.

    Outputs
    ------------
    d       
        the residual sum of squared errors, normalized according to a
        measure of the scale of X, ((X - X.mean(0))**2).sum()

    Z
        the matrix of transformed Y-values

    tform   
        a dict specifying the rotation, translation and scaling that
        maps X --> Y

    """

    n,m = X.shape
    ny,my = Y.shape

    muX = X.mean(0)
    muY = Y.mean(0)

    X0 = X - muX
    Y0 = Y - muY

    ssX = (X0**2.).sum()
    ssY = (Y0**2.).sum()

    # centred Frobenius norm
    normX = np.sqrt(ssX)
    normY = np.sqrt(ssY)

    # scale to equal (unit) norm
    X0 /= normX
    Y0 /= normY

    if my < m:
        Y0 = np.concatenate((Y0, np.zeros(n, m-my)),0)

    # optimum rotation matrix of Y
    A = np.dot(X0.T, Y0)
    U,s,Vt = np.linalg.svd(A,full_matrices=False)
    V = Vt.T
    T = np.dot(V, U.T)

    if reflection is not 'best':

        # does the current solution use a reflection?
        have_reflection = np.linalg.det(T) < 0

        # if that's not what was specified, force another reflection
        if reflection != have_reflection:
            V[:,-1] *= -1
            s[-1] *= -1
            T = np.dot(V, U.T)

    traceTA = s.sum()

    if scaling:

        # optimum scaling of Y
        b = traceTA * normX / normY

        # standarised distance between X and b*Y*T + c
        d = 1 - traceTA**2

        # transformed coords
        Z = normX*traceTA*np.dot(Y0, T) + muX

    else:
        b = 1
        d = 1 + ssY/ssX - 2 * traceTA * normY / normX
        Z = normY*np.dot(Y0, T) + muX

    # transformation matrix
    # if my < m:
        # T = T[:my,:]
    # c = muX - b*np.dot(muY, T)

    #transformation values 
    # tform = {'rotation':T, 'scale':b, 'translation':c}

    return Z

# Import Daily returns and convert to weekly returns
dataset_USD = pd.read_csv('C:/Users/yz283/Documents/MS_challenge/FX_data/FX Data - USD crosses.csv')
df_USD = pd.DataFrame(dataset_USD)
df_USD=df_USD.set_index(df_USD.Date)
df_USD=df_USD.drop('Date',1)
df_USD=df_USD/100+1
for i in range(1,2666,5):
	df_USD.iloc[i,:]=df_USD.iloc[i,:]*df_USD.iloc[i+1,:]*df_USD.iloc[i+2,:]*df_USD.iloc[i+3,:]*df_USD.iloc[i+4,:]
df=(df_USD.iloc[range(1,2666,5),:]-1)*100
df=df[np.abs(df)<13]
df=df.dropna()
df=df[::-1]

# Whole sample loadings
df2=df
cov_mat2 = np.cov(df2.T)
eig_val_cov2, eig_vec_cov2 = np.linalg.eig(cov_mat2)
eig_pairs2 = [(np.abs(eig_val_cov2[i]), eig_vec_cov2[:,i], i) for i in range(len(eig_val_cov2))]
eig_pairs2.sort()
eig_pairs2.reverse()
matrix_wholesample = np.hstack((eig_pairs2[0][1].reshape(len(eig_vec_cov2[:,0]),1),
                    eig_pairs2[1][1].reshape(len(eig_vec_cov2[:,0]),1),
					eig_pairs2[2][1].reshape(len(eig_vec_cov2[:,0]),1),
					eig_pairs2[3][1].reshape(len(eig_vec_cov2[:,0]),1),
					eig_pairs2[4][1].reshape(len(eig_vec_cov2[:,0]),1)))

# Stablize loadings using Procrustes rotation
loadings=[]
for j in range(54,530):
	df1=df[j-27:j]
	df2=df[j-54:j]
	cov_mat1 = np.cov(df1.T)
	cov_mat2 = np.cov(df2.T)
	eig_val_cov1, eig_vec_cov1 = np.linalg.eig(cov_mat1)
	eig_val_cov2, eig_vec_cov2 = np.linalg.eig(cov_mat2)
	eig_pairs1 = [(np.abs(eig_val_cov1[i]), eig_vec_cov1[:,i], i) for i in range(len(eig_val_cov1))]
	eig_pairs2 = [(np.abs(eig_val_cov2[i]), eig_vec_cov2[:,i], i) for i in range(len(eig_val_cov2))]
	eig_pairs1.sort()
	eig_pairs2.sort()
	eig_pairs1.reverse()
	eig_pairs2.reverse()
	matrix_w1 = np.hstack((eig_pairs1[0][1].reshape(len(eig_vec_cov1[:,0]),1),
                      eig_pairs1[1][1].reshape(len(eig_vec_cov1[:,0]),1),
					  eig_pairs1[2][1].reshape(len(eig_vec_cov1[:,0]),1),
					  eig_pairs1[3][1].reshape(len(eig_vec_cov1[:,0]),1),
					  eig_pairs1[4][1].reshape(len(eig_vec_cov1[:,0]),1)))
	matrix_w2 = np.hstack((eig_pairs2[0][1].reshape(len(eig_vec_cov2[:,0]),1),
                      eig_pairs2[1][1].reshape(len(eig_vec_cov2[:,0]),1),
					  eig_pairs2[2][1].reshape(len(eig_vec_cov2[:,0]),1),
					  eig_pairs2[3][1].reshape(len(eig_vec_cov2[:,0]),1),
					  eig_pairs2[4][1].reshape(len(eig_vec_cov2[:,0]),1)))
	matrix_w2=procrustes(matrix_wholesample,matrix_w2)
	matrix_w1=procrustes(matrix_w2,matrix_w1)
	loadings.append(matrix_w1[:,0])
loadings=pd.DataFrame(loadings,columns=df.columns)
# plt.plot(loadings)
# plt.show()
# print (loadings)

# Regress PC against major benchmarks
transformed = np.dot(matrix_wholesample.T, df.T).T
transformed = pd.DataFrame(transformed,columns=['PC1','PC2','PC3','PC4','PC5'],index=df.index)

etf = pd.read_csv('C:/Users/yz283/Documents/MS_challenge/FX_data/ETFs.csv')
for i in list(set(etf.Ticker)): # find unique ticker
	e=etf[etf.Ticker==i]
	e=pd.DataFrame(e)
	list=[]
	for j in transformed.index:
		if any(e.Date==j):
			int = e.index[0]
			ind = e[e['Date']==j].index.tolist()
			if ind[0] > 5 + int:
				list.append(e.loc[ind[0],'Adj Open']/e.loc[ind[0]-5,'Adj Open']-1)
			else:
				list.append(0)
		else:
			list.append(0)
	transformed[i]=pd.Series(list,index=transformed.index)
corr=np.corrcoef(transformed.T)
plt.plot(corr[0])
plt.show()