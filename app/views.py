from flask import Flask
from flask import request
from flask import render_template
from app import app

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/avg')
def my_form():
    return render_template("avg_form.html")

@app.route('/avg/answer', methods=['POST'])
def my_form_post():

    numbers=[]
    try:
        numbers=[float(i) for i in request.form['list'].split()]
    except:
        return render_template("avg_error.html")

    if(len(numbers)==0):
        return render_template("avg_error.html", empty="True")
    average=sum(numbers)/len(numbers)
    return render_template("avg_result.html",answer=average,numbers=numbers)

@app.route('/polynomial')
def get_data():
    return render_template("poly_form.html")

@app.route('/polynomial/answer', methods=['POST'])
def find_polynomial():

    from numpy import array,arange    
    from numpy.polynomial import polynomial as P    
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import os, sys

    try:
        x=[float(i) for i in request.form['x_values'].split()]
        y=[float(i) for i in request.form['f(x)_values'].split()]
    except:
        return render_template("poly_error.html")
    if(len(x)!=len(y)):
        return render_template("poly_error.html",mismatch="True")
    if(len(x)*len(y)==0):
        return render_template("poly_error.html",empty="True")

    def Lagrange(L,M):                                                               
        polylist=[]
        n=len(L)                                                           
        w=(-1*L[0],1)                                                      
        for i in range(1,n):
            w=P.polymul(w,(-1*L[i],1))                                    
        result=array([0.0 for i in range(len(w)-1)])                    
        derivative=P.polyder(w)                                             
        for i in range(n):
            polylist.append((P.polydiv(w,(-1*L[i],1))[0]*M[i])/P.polyval(L[i],derivative))
            result+=polylist[-1]   

        polynomial=""                                                  
        for i in range(len(result)-1,0,-1):                                 
            if(result[i]!=0):
                if(result[i]>0 and i!=(len(result)-1)):
                    polynomial+=" + "+str(result[i])+"x^"+str(i)+" "
                elif(result[i]>0 and i==(len(result)-1)):
                    polynomial+=str(result[i])+"x^"+str(i)+" "
                else:
                    polynomial+=" - "+str(-1*result[i])+"x^"+str(i)+" "
        if(result[0]!=0):
            polynomial+=" + "+str(result[0]) if result[0]>0 else " - "+str(-1*result[0])
        plot(L,M,polylist,result)
        return (polynomial)

    def plot(x_values,y_values,polylist,result):                
        fig=plt.figure()
        Color=["b","g","r","y","m"]                                         
        Legend=[]                                                           
        for i in range(len(polylist)):                                 
            x=list(arange(min(x_values)-1,max(x_values)+1,0.01))
            y=list(map(lambda num:P.polyval(num,polylist[i]),x))
            plt.plot(x,y,linewidth=2.0,color=Color[i%5])
            Legend.append(mpatches.Patch(color=Color[i%5],label="Polynomial "+str(i+1)))    
        x=list(arange(min(x_values)-1,max(x_values)+1,0.01))
        y=list(map(lambda num:P.polyval(num,array(result)),x))
        plt.plot(x,y,linewidth=3.0,color="k")                               
        Legend.append(mpatches.Patch(color="k",label="Final polynomial"))   
        x=x_values
        y=list(map(lambda num:P.polyval(num,array(result)),x))         
        plt.plot(x,y,"o",color="c")                                         
        plt.axvline(0,color="k")
        plt.axhline(0,color="k")
        plt.xlabel(" x values ")
        plt.ylabel("f(x) values")
        plt.legend(handles=Legend)
        dir=sys.path[0]
        dir+="\\app\\static\\graph.png" 
        if os.path.exists(dir):
            os.remove(dir)
            plt.savefig(dir, format="png", dpi=fig.dpi)
        else:             
            plt.savefig(dir, format="png", dpi=fig.dpi)                                                                                         

    return render_template("poly_result.html",answer=Lagrange(x,y),x=x,y=y) 

@app.route('/info')
def display():
    return render_template("info.html") 

@app.route('/info/ujjwal')
def display_ujjwal():
    return render_template("ujjwal.html") 

@app.route('/info/atishay')
def display_atishay():
    return render_template("atishay.html") 

@app.route('/info/digvijay')
def display_digvijay():
    return render_template("digvijay.html") 
                                        
