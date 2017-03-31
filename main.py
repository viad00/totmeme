from functools import wraps
from flask import Flask, request, Response, render_template, redirect, flash
import datetime
import hashlib
import forms
import models

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'd39jo390cdeoijfer903fwb9u0j28e'
app.config['password'] = 'a97958817751e4401ae0a25501e1a39b21433ba8b7514f94e03ca6014bcee12b'


def check_auth(username, password):
    return (username == 'admin' and hashlib.sha256('sae' + password + 'hau').hexdigest() == app.config['password']) \
           or onelog(username, password) or login(username, password)


def onelog(username, password):
    saas = '6' + (datetime.datetime.now() + datetime.timedelta(hours=3)).strftime('%d%H%M') + '7'
    if password == saas: models.Visit(user_ip=request.remote_addr, action='USED ONELOG').put()
    return username == 'onelog' and password == saas


def login(username, password):
    if models.User.query(models.User.username == username and models.User.password == hashlib.sha256(
                            'sae' + password + 'hau').hexdigest()).count() > 0:
        kkk = models.User.query(models.User.username == username).fetch()
        for kk in kkk:
            kk.lastlogin = datetime.datetime.now()
            kk.put()
        return True
    else:
        return False


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@app.route('/')
def hello_world():
    return 'Remember it?'


@app.route('/admin')
@requires_auth
def admin():
    problems = []
    try:
        dev = models.Device.query(models.Device.lastseen < datetime.datetime.now() - datetime.timedelta(minutes=4))
        if dev.count() > 0:
            for de in dev.fetch():
                problems.append('Device ' + de.name + ' is not seen in 4 minutes')
        dev = models.Server.query(models.Server.lastseen < datetime.datetime.now() - datetime.timedelta(minutes=4))
        if dev.count() > 0:
            for de in dev.fetch():
                problems.append('Server ' + de.name + ' is not seen in 4 minutes')
    except Exception as e:
        flash('cannot check: ' + str(e))
    logins = models.Visit.query().order(-models.Visit.timestamp).fetch(limit=10)
    return render_template('admin.html', problems=problems, logins=logins)


@app.route('/admin/addtask', methods=('GET', 'POST'))
@requires_auth
def addtask():
    form = forms.AddTask()
    if form.validate_on_submit():
        mom = models.Task(controller=request.form['controller'],
                          target=request.form['target'],
                          action=request.form['action'])
        mom.put()
        models.Visit(user_ip=request.remote_addr, action='PUT TASK ' + str(mom.key.integer_id())).put()
        flash('added ' + str(mom.key.integer_id()))
        return redirect('/admin/tasks')
    return render_template('addtask.html', form=form)


@app.route('/admin/tasks')
@requires_auth
def tasks():
    tasks = models.Task.query().order(-models.Task.timestamp).fetch(limit=10)
    return render_template('tasks.html', tasks=tasks)


@app.route('/admin/deltask')
@requires_auth
def deltask():
    try:
        id = int(request.args.get('id'))
    except Exception:
        flash('Get param failed!')
        return redirect('/admin/tasks')
    try:
        models.Task.get_by_id(id).key.delete()
        models.Visit(user_ip=request.remote_addr, action='DEL TASK ' + str(id)).put()
        flash('Successful delete of ' + str(id))
    except Exception:
        models.Visit(user_ip=request.remote_addr, action='DEL TASK FAILED ' + str(id)).put()
        flash('Delete failed! ' + str(id))
    return redirect('/admin/tasks')


@app.route('/admin/adddevice', methods=('GET', 'POST'))
@requires_auth
def adddevice():
    form = forms.AddDevice()
    if form.validate_on_submit():
        mom = models.Device(name=request.form['name'])
        mom.put()
        models.Visit(user_ip=request.remote_addr, action='PUT DEVICE ' + str(mom.key.integer_id())).put()
        flash('added ' + str(mom.key.integer_id()))
        return redirect('/admin/devices')
    return render_template('adddevice.html', form=form)


@app.route('/admin/devices')
@requires_auth
def devices():
    dev = models.Device.query().order(-models.Device.lastseen).fetch()
    return render_template('devices.html', devices=dev)


@app.route('/admin/deldevice')
@requires_auth
def deldevice():
    try:
        id = int(request.args.get('id'))
    except Exception:
        flash('Get param failed!')
        return redirect('/admin/devices')
    try:
        models.Device.get_by_id(id).key.delete()
        models.Visit(user_ip=request.remote_addr, action='DEL DEVICE ' + str(id)).put()
        flash('Successful delete of ' + str(id))
    except Exception:
        models.Visit(user_ip=request.remote_addr, action='DEL DEVICE FAILED ' + str(id)).put()
        flash('Delete failed! ' + str(id))
    return redirect('/admin/devices')


@app.route('/admin/addserver', methods=('GET', 'POST'))
@requires_auth
def addserver():
    form = forms.AddServer()
    if form.validate_on_submit():
        mom = models.Server(name=request.form['name'],
                            controller=request.form['controller'],
                            pin=request.form['pin'],
                            lastseen=datetime.datetime.now())
        mom.put()
        models.Visit(user_ip=request.remote_addr, action='PUT SERVER ' + str(mom.key.integer_id())).put()
        flash('added ' + str(mom.key.integer_id()))
        return redirect('/admin/servers')
    return render_template('addserver.html', form=form)


@app.route('/admin/servers')
@requires_auth
def servers():
    dev = models.Server.query().order(-models.Server.lastseen).fetch()
    return render_template('servers.html', servers=dev)


@app.route('/admin/delserver')
@requires_auth
def delserver():
    try:
        id = int(request.args.get('id'))
    except Exception:
        flash('Get param failed!')
        return redirect('/admin/servers')
    try:
        models.Server.get_by_id(id).key.delete()
        models.Visit(user_ip=request.remote_addr, action='DEL SERVER ' + str(id)).put()
        flash('Successful delete of ' + str(id))
    except Exception:
        models.Visit(user_ip=request.remote_addr, action='DEL SERVER FAILED ' + str(id)).put()
        flash('Delete failed! ' + str(id))
    return redirect('/admin/servers')


@app.route('/get_routines')
def routines():
    try:
        controller = request.args.get('controller')
    except Exception:
        return 'ERROR REPORT'
    try:
        query = models.Device.query(models.Device.name == controller)
        if query.count() > 0:
            for dev in query.fetch():
                dev.lastseen = datetime.datetime.now()
                dev.put()
        else:
            return '0'
    except Exception as e:
        print 'Caught exp at get_routines: ' + str(e)
        return 'ERROR CHECK'
    try:
        tasken = models.Task.query(models.Task.controller == controller, models.Task.done == False).order(
            models.Task.timestamp)
        dev = models.Server.query(models.Server.lastseen < datetime.datetime.now() - datetime.timedelta(minutes=4),
                                  models.Server.controller == controller)
        device = models.Device.query(models.Device.lastseen < datetime.datetime.now() - datetime.timedelta(minutes=4)).count()
        if dev.count() > 0 and tasken.count() < 1 and device < 1:
            for de in dev.fetch():
                models.Task(controller=de.controller, target=de.pin, action='stop').put()
                models.Task(controller=de.controller, target=de.pin, action='start').put()
                models.Visit(user_ip=request.remote_addr, action='ADD TASK TO START ' + de.name).put()
        tasken = tasken.fetch()
    except Exception as e:
        print 'Caught exp at get_routines: ' + str(e)
        return 'ERROR DATABASE'
    ret = str(len(tasken)) + '\n'
    for task in tasken:
        mmm = str(task.key.integer_id()) + '; '
        mmm += str(task.target) + '; '
        mmm += str(task.action) + '; '
        mmm += '\n'
        ret += mmm
    return ret


@app.route('/callback')
def callback():
    try:
        action = request.args.get('action')
    except Exception:
        return 'ERROR REPORT'
    if action == 'done':
        try:
            idd = int(request.args.get('id'))
            note = request.args.get('note')
            tas = models.Task.get_by_id(idd)
            tas.done = True
            tas.notes = note
            tas.put()
            models.Visit(user_ip=request.remote_addr, action='REPORTED ' + str(tas.key.integer_id())).put()
            return 'OK'
        except Exception:
            return 'ERROR OK'
    elif action == 'server':
        try:
            name = request.args.get('name')
            serves = models.Server.query(models.Server.name == name).fetch()
            for server in serves:
                server.lastseen = datetime.datetime.now()
                server.put()
            return 'OK'
        except Exception as e:
            print 'Error call server: ' + str(e)
            return 'ERROR OK'


@app.route('/admin/flush_all')
@requires_auth
def flush_all():
    try:
        cc = models.Visit.query().count()
        for key in models.Visit.query().fetch(keys_only=True):
            key.delete()
        flash('Flushed all ' + str(cc) + ' entries!')
    except Exception as e:
        flash('Cannot flush: ' + str(e))
    return redirect('/admin')


@app.route('/admin/adduser', methods=('GET', 'POST'))
@requires_auth
def adduser():
    form = forms.AddUser()
    if form.validate_on_submit():
        mom = models.User(username=request.form['username'],
                          password=hashlib.sha256('sae' + request.form['password'] + 'hau').hexdigest())
        mom.put()
        models.Visit(user_ip=request.remote_addr, action='PUT USER ' + str(mom.key.integer_id())).put()
        flash('Add user ' + request.form['username'])
        return redirect('/admin/users')
    return render_template('adduser.html', form=form)


@app.route('/admin/users')
@requires_auth
def users():
    users = models.User.query().order(-models.User.timestamp).fetch()
    return render_template('users.html', users=users)


@app.route('/admin/deluser')
@requires_auth
def deluser():
    try:
        id = int(request.args.get('id'))
    except Exception:
        flash('Get param failed!')
        return redirect('/admin/users')
    try:
        models.User.get_by_id(id).key.delete()
        models.Visit(user_ip=request.remote_addr, action='DEL USER ' + str(id)).put()
        flash('Successful delete of ' + str(id))
    except Exception:
        models.Visit(user_ip=request.remote_addr, action='DEL USER FAILED ' + str(id)).put()
        flash('Delete failed! ' + str(id))
    return redirect('/admin/users')


if __name__ == '__main__':
    app.run()
