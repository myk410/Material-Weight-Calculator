const {readFileSync} = require('node:fs');
const {join} = require('node:path');
const {runInNewContext} = require('node:vm');
const assert = require('node:assert/strict');
const html = readFileSync(join(__dirname, '../Material-Weight-Calculator.html'), 'utf8');
const elements = new Map();
function element(id) {
 if (!elements.has(id)) elements.set(id, {value:'', textContent:'', hidden:false, open:false, children:[], handlers:{},
  addEventListener(name, fn){this.handlers[name]=fn;}, appendChild(child){this.children.push(child);}});
 return elements.get(id);
}
element('material').value='steel';
element('shape').value='rectangle';
element('pipeMethod').value='wall';
const context = {document:{getElementById:element, createElement:()=>({children:[],appendChild(child){this.children.push(child);}})}};
runInNewContext(html.match(/<script>([\s\S]*?)<\/script>/)[1], context);
const near = (actual, expected) => assert.ok(Math.abs(actual-expected)<1e-10, `${actual} != ${expected}`);
const pipe={pipeLength:12,outsideDiameter:2,pipeSize:0.125,pipeMethod:'wall'};
near(context.weightFromVolume(context.calculateVolume('rectangle',{length:12,width:12,thickness:1}),490),490/12);
const volume=context.calculateVolume('pipe',pipe);
near(volume,Math.PI/4*(4-1.75**2)*12);
near(context.weightFromVolume(volume,490),2.50550195354655);
near(context.calculateVolume('pipe',{...pipe,pipeSize:1.75,pipeMethod:'inside'}),volume);
near(context.calculateVolume('volume',{volume:1728}),1728);
for (const size of [0,-1,1,2,'',Infinity]) assert.throws(()=>context.calculateVolume('pipe',{...pipe,pipeSize:size}));
for (const size of [0,-1,2,3,'',Infinity]) assert.throws(()=>context.calculateVolume('pipe',{...pipe,pipeSize:size,pipeMethod:'inside'}));
assert.throws(()=>context.calculateVolume('rectangle',{length:'',width:1,thickness:1}));
assert.throws(()=>context.weightFromVolume(Infinity,490));
assert.throws(()=>context.weightFromVolume(1,0));
assert.throws(()=>context.weightFromVolume(1e308,490));
const published={poly:57.43372485,hdpe:59.30656240,water:62.424,aluminum:169.344,titanium:281.664,steel:490.05949064,stainless:492.48,stainless316:499.392,inconel:511.488,inconel625:527.04,brass:532.224,cuni:558.144,cuni7030:558.144,nicu:549.504,lead:706.752};
for (const [name,density] of Object.entries(published)) {
 element('material').value=name;context.updateMaterial();assert.ok(Math.abs(Number(element('density').value)-density)<0.00001, name);
}
assert.equal(element('densityTable').children.length,15);
element('material').value='titanium';context.updateMaterial();
near(context.weightFromVolume(1728,element('density').value),281.664);
assert.notEqual(Number(element('density').value),168);
element('shape').value='pipe';context.updateShape();assert.equal(element('rectangleFields').hidden,true);assert.equal(element('pipeFields').hidden,false);
element('material').value='steel';context.updateMaterial();
for (const [id,value] of Object.entries(pipe)) element(id).value=String(value);
context.calculateWeight();assert.match(element('result').textContent,/2\.51 lb/);assert.match(element('result').textContent,/Published preset: 490.059/);
element('density').value='281.664';context.calculateWeight();assert.match(element('result').textContent,/Density override/);
element('pipeSize').value='1';context.calculateWeight();assert.equal(element('result').textContent,'');assert.match(element('error').textContent,/less than half/);
element('pipeMethod').value='inside';context.updatePipeMethod();assert.equal(element('pipeSize').value,'');assert.match(element('pipeSizeLabel').textContent,/Inside diameter/);
element('material').value='custom';context.updateMaterial();assert.equal(element('densitySettings').open,true);assert.equal(element('density').value,'');
console.log('Passed: published grade densities and titanium correction, rectangular/pipe/volume formulas, OD/wall and OD/ID equivalence, validation, override labeling, and UI state transitions.');
