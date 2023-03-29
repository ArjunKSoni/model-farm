from flask import Flask,render_template,flash,redirect,request,  jsonify
app = Flask(__name__)
import soil
import search_crop as sc
import crop_json as cj
import crop
model_soi,ind,df1=soil.model()
model_cr,inde2=crop.model()
model_soil=model_soi
index=ind
df=df1
model_crop=model_cr
index2=inde2

@app.route('/', methods=['GET'])
def mainpage():
    return "api is live broooo"

@app.route('/nav', methods=['POST'])
def nav():
    crop=request.body['search']
    p=sc.search(crop)
    if p==-1:
        return jsonify({"status":"fail"})
    k=df[df['label']==p[0]]['Sno'].values
    crop_detail=[]
    crop_img=[]
    crop_name=[]
    pi=[]
    for i in range(4):
        crop_detail.append(cj.find(p[i]))
        crop_img.append(crop_detail[i]["img"])
        crop_name.append(crop_detail[i]["name"].upper())
    crop_desc=crop_detail[0]["desc"]
    pi=df[df['Sno']==k[0]].values[0]
    return jsonify({"crop":pi, "ci":crop_img, "cn":crop_name, "cd":crop_desc})


@app.route('/get_soil_info', methods=['GET', 'POST'])
def get_soil_info():
    if (request.method == 'POST'):
        N=int(request.body['N'])
        P=int(request.body['P'])
        K=int(request.body['K'])
        temperature=int(request.body['temperature'])
        humidity=int(request.body['humidity'])
        ph=int(request.body['ph'])
        rainfall=int(request.body['rainfall'])
        label=(request.body['label'])
        val=[N,P,K,temperature,humidity,ph,rainfall]
        p=sc.search(label)
        if p==-1:
            return jsonify({"status":"fail"})   #not found pg
        global inde
        for i in index:
            if(i[0]==p[0]):
                val.append(i[1])
                break
        predicted=soil.predict(val,model_soil,index)

        
        crop_detail=[]
        crop_img=[]
        crop_name=[]
        for i in range(4):
            crop_detail.append(cj.find(p[i]))
            crop_img.append(crop_detail[i]["img"])
            crop_name.append(crop_detail[i]["name"].upper())
        crop_desc=crop_detail[0]["desc"]

        return jsonify({"crop":predicted, "ci":crop_img, "cn":crop_name, "cd":crop_desc})
    
    else:
        return jsonify({"status":"fail"})

@app.route('/get_crop_info', methods=['GET', 'POST'])
def get_crop_info():
    if request.method == 'POST':
        N=int(request.body['N'])
        P=int(request.body['P'])
        K=int(request.body['K'])
        temperature=int(request.body['temperature'])
        humidity=int(request.body['humidity'])
        ph=int(request.body['ph'])
        rainfall=int(request.body['rainfall'])
        val=[N,P,K,temperature,humidity,ph,rainfall]
        predicted=crop.predict(val,model_crop,index2)
        # crops=[]
        p=sc.search(predicted[8])
        if p==-1:
            return jsonify({"status":"fail"})   #not found pg
        crop_detail=[]
        crop_img=[]
        crop_name=[]
        for i in range(4):
            crop_detail.append(cj.find(p[i]))
            crop_img.append(crop_detail[i]["img"])
            crop_name.append(crop_detail[i]["name"].upper())
        crop_desc=crop_detail[0]["desc"]

        return jsonify({"crop":predicted, "ci":crop_img, "cn":crop_name, "cd":crop_desc})  

    else:
        return jsonify({"status":"fail"})

# if __name__ == "__main":
app.run(debug=False)