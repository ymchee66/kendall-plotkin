/* Simulated annealing search for permutation codes attaining the Plotkin bound.
   Finds M permutations of length n, pairwise at Kendall tau-distance exactly D = m*C(n,2)/(2m-1),
   with every pair of symbols split as evenly as possible.
   Usage: sa n M seed iters_millions [T0 T1]
   Example: ./sa 8 8 1 200 1.5 0.5 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define MAXN 64
#define MAXM 32

static int n, M, m, D;
static int ord[MAXM][MAXN], pos[MAXM][MAXN];
static int split[MAXN][MAXN];      /* split[a][b], a<b: codewords placing a before b */
static int dist[MAXM][MAXM];

static unsigned long long rng;
static inline unsigned long long xr(void){ rng ^= rng<<13; rng ^= rng>>7; rng ^= rng<<17; return rng; }
static inline double ur(void){ return (xr()>>11)*(1.0/9007199254740992.0); }

static inline int splitcost(int s){
  if (M%2==0) return abs(s-m);
  if (s<m-1) return m-1-s;
  if (s>m) return s-m;
  return 0;
}

static long total_cost(void){
  long c=0;
  for(int k=0;k<M;k++) for(int l=k+1;l<M;l++) c+=abs(dist[k][l]-D);
  for(int a=0;a<n;a++) for(int b=a+1;b<n;b++) c+=splitcost(split[a][b]);
  return c;
}

static void init(void){
  for(int k=0;k<M;k++){
    for(int i=0;i<n;i++) ord[k][i]=i;
    for(int i=n-1;i>0;i--){ int j=xr()%(i+1); int t=ord[k][i]; ord[k][i]=ord[k][j]; ord[k][j]=t; }
    for(int i=0;i<n;i++) pos[k][ord[k][i]]=i;
  }
  memset(split,0,sizeof split);
  for(int a=0;a<n;a++) for(int b=a+1;b<n;b++)
    for(int k=0;k<M;k++) if(pos[k][a]<pos[k][b]) split[a][b]++;
  for(int k=0;k<M;k++) for(int l=0;l<M;l++){
    int c=0;
    if(k!=l) for(int a=0;a<n;a++) for(int b=a+1;b<n;b++)
      if((pos[k][a]<pos[k][b])!=(pos[l][a]<pos[l][b])) c++;
    dist[k][l]=c;
  }
}

int main(int argc,char**argv){
  n=atoi(argv[1]); M=atoi(argv[2]); rng=strtoull(argv[3],0,10)*2654435761ULL+1;
  long long maxit=(long long)(atof(argv[4])*1e6);
  int C=n*(n-1)/2; m=(M+1)/2;
  if((m*C)%(2*m-1)){ printf("D not integer\n"); return 1; }
  D=m*C/(2*m-1);
  for(int restart=0;;restart++){
    init();
    long cost=total_cost(), best=cost;
    double T0=argc>5?atof(argv[5]):2.0, T1=argc>6?atof(argv[6]):0.02;
    long long it;
    for(it=0; it<maxit && cost>0; it++){
      double T=T0*pow(T1/T0,(double)it/maxit);
      int k=xr()%M, i=xr()%(n-1);
      int a=ord[k][i], b=ord[k][i+1];        /* a currently before b in codeword k */
      int lo=a<b?a:b, hi=a<b?b:a;
      int s=split[lo][hi];
      int ns = (a<b) ? s-1 : s+1;            /* after swap */
      long delta = splitcost(ns)-splitcost(s);
      for(int l=0;l<M;l++) if(l!=k){
        int agree = pos[l][a]<pos[l][b];     /* l agrees with k before swap */
        int nd = dist[k][l] + (agree?1:-1);
        delta += abs(nd-D)-abs(dist[k][l]-D);
      }
      if(delta<=0 || ur()<exp(-delta/T)){
        ord[k][i]=b; ord[k][i+1]=a; pos[k][a]=i+1; pos[k][b]=i;
        split[lo][hi]=ns;
        for(int l=0;l<M;l++) if(l!=k){
          int agree_after = pos[l][a]<pos[l][b] ? 0 : 1; /* now k has b above a */
          /* recompute sign: before swap k had a above b. */
          int lagrees_before = pos[l][a]<pos[l][b];
          int nd = dist[k][l] + (lagrees_before?1:-1);
          (void)agree_after;
          dist[k][l]=dist[l][k]=nd;
        }
        cost+=delta; if(cost<best) best=cost;
      }
    }
    if(cost==0){
      printf("FOUND n=%d M=%d D=%d restart=%d it=%lld\n",n,M,D,restart,it);
      for(int k=0;k<M;k++){ for(int i=0;i<n;i++) printf("%d%c",ord[k][i],i==n-1?'\n':' '); }
      fflush(stdout); return 0;
    }
    fprintf(stderr,"restart %d best %ld\n",restart,best);
  }
}
