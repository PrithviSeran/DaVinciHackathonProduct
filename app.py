import os
import openai
from flask import Flask,render_template, request, redirect, flash
import pandas as pd
import random
import csv

  
app = Flask(__name__) 


wanted_service = ""
customer_needs = {}
service_provider_info = {}
service_cost = {}

openai.api_key = "API_KAY"

@app.route("/", methods=["GET", "POST"]) 
def index(): 
    global wanted_service
    if request.method == "POST":
       
        if request.form["action"] == "Join-Now1":

          wanted_service = request.form["fname"]

          return render_template("create_an_account.html")
        
        if request.form["action"] == "Nanny" or request.form["action"] == "Barber" or request.form["action"] == "Grocery-Shopper" or request.form["action"] == "Housekeeper" or request.form["action"] == "Plumber":
             wanted_service = "I need a " + request.form["action"] + "."

             return render_template("create_an_account.html")

        if request.form["action"] == "Join-Now":
          return render_template("fill_info.html")
        
        if request.form["action"] == "Home":
          return redirect("/")
        
        if request.form["action"] == "About":
          return redirect("/about")
        
        if request.form["action"] == "Contact":
          return render_template("/contact")
        


        #return render_template("fill_info.html")
    
    return render_template("main_page.html")

@app.route("/create_an_account", methods=["GET", "POST"]) 
def create_an_account(): 
    global wanted_service
    global customer_needs
    if request.method == "POST":
       if request.form["action"] == "Home":
          return redirect("/")
        
       if request.form["action"] == "About":
          return redirect("/about")
        
       if request.form["action"] == "Contact":
          return redirect("/contact")
       
       customer_needs = {
          "Need": wanted_service,
          "Full Name": request.form["fname"],
          "Email": request.form["email"],
          "Phone Number": request.form["phone-number"],
          "Description": request.form["description"]
       }

       return redirect("/booking_service")
    
    return render_template("create_an_account.html")

@app.route("/booking_service", methods=["GET", "POST"]) 
def booking_service(): 
    global customer_needs

    if request.method == "POST":
       if request.form["action"] == "Home":
          return redirect("/")
        
       if request.form["action"] == "About":
          return redirect("/about")
        
       if request.form["action"] == "Contact":
          return redirect("/contact")
       
       return render_template("payment.html")
    
    f = open("service_descriptions.txt", "r")

    g = open("needs_descriptions.txt", "a")
    g.write("\n\n\n\n\n" + customer_needs["Need"])
    g.close()

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "When a person has been chosen, output their description from the input."},
        {"role": "user", "content": "Choose the best person among these people to tend this need. Also Explain why they are the best for this need and how much they charge: " + customer_needs["Need"] + " \n" + f.read()}
      ]
    )
    
    return render_template("booking_service.html", best_match=completion["choices"][0]["message"]["content"])

@app.route("/payment", methods=["GET", "POST"]) 
def payment(): 

    if request.method == "POST":
       if request.form["action"] == "Home":
          return redirect("/")
        
       if request.form["action"] == "About":
          return redirect("/about")
        
       if request.form["action"] == "Contact":
          return redirect("/contact")

       return render_template("thanks.html")
    
    return render_template("payment.html")

    #return render_template("booking_service.html")

@app.route("/fill_info", methods=["GET", "POST"]) 
def fill_info(): 
    global service_provider_info

    if request.method == "POST":
       if request.form["action"] == "Home":
          return redirect("/")
        
       if request.form["action"] == "About":
          return redirect("/about")
        
       if request.form["action"] == "Contact":
          return redirect("/contact")
       
       service_provider_info["Full Name"] = request.form["full-name"]
       service_provider_info["Display Name"] = request.form["display-name"]
       service_provider_info["Description"] = request.form["description"]
       service_provider_info["Languages"] = request.form["languages"]

       return render_template("professional_info.html")
    
    return render_template("fill_info.html")

@app.route("/professional_info", methods=["GET", "POST"]) 
def professional_info(): 
    if request.method == "POST":
       if request.form["action"] == "Home":
          return redirect("/")
        
       if request.form["action"] == "About":
          return redirect("/about")
        
       if request.form["action"] == "Contact":
          return redirect("/contact")
       

       service_provider_info["Occupation"] = request.form["occupation"]
       service_provider_info["Skills"] = request.form["skills"]
       service_provider_info["Education"] = request.form["education"]
       service_provider_info["Certifications"] = request.form["certifications"]
       service_provider_info["Linked Accounts"] = request.form["linked-accounts"]
       service_provider_info["Payment"] = request.form["payment"]
       service_provider_info["Price"] = request.form["payment"]

       return render_template("security_check.html")
    
    return render_template("professional_info.html")

@app.route("/security_check", methods=["GET", "POST"]) 
def security_check(): 
    global service_provider_info
    if request.method == "POST":
       
       if request.form["action"] == "Home":
          return redirect("/")
        
       if request.form["action"] == "About":
          return redirect("/about")
        
       if request.form["action"] == "Contact":
          return redirect("/contact")
       
       string_service_provider_info = str(service_provider_info)

       completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "user", "content": "Write a sentence describing this person based on these descriptions and Payment: " + string_service_provider_info}
        ]
       )
       
       f = open("service_descriptions.txt", "a")
       f.write("\n\n\n\n\n" + completion["choices"][0]["message"]["content"])
       f.close()
       
       return redirect("/business")
    
    return render_template("security_check.html")

@app.route("/business", methods=["GET", "POST"]) 
def business(): 
    if request.method == "POST":
      if request.form["action"] == "Home":
        return redirect("/")
        
      if request.form["action"] == "About":
        return redirect("/about")
        
      if request.form["action"] == "Contact":
        return redirect("/contact")
      

    string_service_provider_info = str(service_provider_info)

    f = open("needs_descriptions.txt", "r")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "user", "content": "Choose the most suitable request among these: \n" + f.read() + " which can be fulfilled by this person: " + string_service_provider_info + " \n"}
        ]
    )
    first_names=('Richard','Andy','Chad')
    last_names=('Shin','Smith','Leo')

    group=" ".join(random.choice(first_names)+" "+random.choice(last_names))

    return render_template("business.html", Need = completion["choices"][0]["message"]["content"], name = group)
    
    #return render_template("business.html")

@app.route("/about", methods=["GET", "POST"])
def about():
   
   if request.method == "POST":
      if request.form["action"] == "Home":
        return redirect("/")
        
      if request.form["action"] == "About":
        return redirect("/about")
        
      if request.form["action"] == "Contact":
        return redirect("/contact")
      
   return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
   
   if request.method == "POST":
      if request.form["action"] == "Home":
        return redirect("/")
        
      if request.form["action"] == "About":
        return redirect("/about")
        
      if request.form["action"] == "Contact":
        return redirect("/contact")
      
   return render_template("contact_us.html")

if __name__=="__main__":
    app.run(debug=True)



