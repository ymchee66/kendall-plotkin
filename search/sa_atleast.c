/* Simulated annealing search for M permutations of length n that are pairwise at
   distance at least D in the Kendall tau-metric (used for Theorem 7.2).
   Example: ./sa_atleast 14 6 54 1 50 1.5 0.3
   Usage: sa_atleast n M D seed iters_millions T0 T1 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#define MAXN 64
#define MAXM 32
static int n,M,D,ord[MAXM][MAXN],pos[MAXM][MAXN],dist[MAXM][MAXM];
static unsigned long long rng;
static inline unsigned long long xr(void){rng^=rng<<13;rng^=rng>>7;rng^=rng<<17;return rng;}
static inline double ur(void){return (xr()>>11)*(1.0/9007199254740992.0);}
static inline int pc(int d){return d<D?D-d:0;}
int main(int argc,char**argv){
  n=atoi(argv[1]);M=atoi(argv[2]);D=atoi(argv[3]);rng=strtoull(argv[4],0,10)*2654435761ULL+7;
  long long maxit=(long long)(atof(argv[5])*1e6); double T0=atof(argv[6]),T1=atof(argv[7]);
  for(int restart=0;;restart++){
    for(int k=0;k<M;k++){for(int i=0;i<n;i++)ord[k][i]=i;for(int i=n-1;i>0;i--){int j=xr()%(i+1),t=ord[k][i];ord[k][i]=ord[k][j];ord[k][j]=t;}for(int i=0;i<n;i++)pos[k][ord[k][i]]=i;}
    long cost=0;
    for(int k=0;k<M;k++)for(int l=k+1;l<M;l++){int c=0;for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)if((pos[k][a]<pos[k][b])!=(pos[l][a]<pos[l][b]))c++;dist[k][l]=dist[l][k]=c;cost+=pc(c);}
    long best=cost; long long it;
    for(it=0;it<maxit&&cost>0;it++){
      double T=T0*pow(T1/T0,(double)it/maxit);
      int k=xr()%M,i=xr()%(n-1),a=ord[k][i],b=ord[k][i+1];
      long delta=0;
      for(int l=0;l<M;l++)if(l!=k){int ag=pos[l][a]<pos[l][b];int nd=dist[k][l]+(ag?1:-1);delta+=pc(nd)-pc(dist[k][l]);}
      if(delta<=0||ur()<exp(-delta/T)){
        for(int l=0;l<M;l++)if(l!=k){int ag=pos[l][a]<pos[l][b];dist[k][l]=dist[l][k]=dist[k][l]+(ag?1:-1);}
        ord[k][i]=b;ord[k][i+1]=a;pos[k][a]=i+1;pos[k][b]=i;cost+=delta;if(cost<best)best=cost;}
    }
    if(cost==0){printf("FOUND n=%d M=%d D=%d restart=%d\n",n,M,D,restart);for(int k=0;k<M;k++)for(int i=0;i<n;i++)printf("%d%c",ord[k][i],i==n-1?'\n':' ');fflush(stdout);return 0;}
    fprintf(stderr,"restart %d best %ld\n",restart,best);
  }
}
