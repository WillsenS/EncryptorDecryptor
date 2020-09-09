import tkinter as tk
from collections import defaultdict
import string


NSEW = tk.N + tk.S + tk.E + tk.W


class VigenereKey(tk.Frame):
    def __init__(self, title, current_key, key_callback, master=None):
        super().__init__(master)
        self.grid(sticky=NSEW)
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.create_widgets(title)
        if current_key is not None:
            self.keyvar.set(current_key)
        self.key = current_key
        self.key_callback = key_callback

    def create_widgets(self, title):
        # Row 0
        tk.Label(self, text=title).grid(columnspan=2)
        # Row 1
        self.keyvar = tk.StringVar()
        keytxt = tk.Entry(self, textvariable=self.keyvar, validate='focus',
                          validatecommand=self.check)
        keytxt.bind('<KeyPress-Return>', self.enter)
        keytxt.grid(columnspan=2)
        keytxt.focus()
        # Row 2
        checklbl = tk.Label(self)
        checklbl.grid(columnspan=2)
        self.checklbl = checklbl
        # Row 3
        check = tk.Button(self, text='Check', command=self.check)
        check.grid()
        ok = tk.Button(self, text='Ok', command=self.submit, state='disabled')
        ok.bind('<KeyPress-Return>', self.enter)
        ok.grid(row=3, column=1)
        self.ok = ok
        self.check()

    def check(self):
        #print('checking', self.keyvar.get())
        key = self.keyvar.get()
        ok = False
        if len(key) < 1:
            self.checklbl.configure(text='Minimum 1 letter')
        elif not all(c in string.ascii_letters for c in key):
            self.checklbl.configure(text='Only letters A-Z allowed')
        else:
            self.checklbl.configure(text='Key OK')
            ok = True
            self.key = key
        self.ok.configure(state='normal' if ok else 'disabled')
        return ok

    def enter(self, event):
        self.submit()

    def submit(self):
        if self.check():
            self.key_callback(self.key)
            self.master.destroy()


class ExtendedVigenereKey(VigenereKey):
    def __init__(self, current_key, key_callback, master=None):
        super().__init__('Extended Vigen\xe8re Key', current_key, key_callback,
                         master)

    def check(self):
        #print('checking', self.keyvar.get())
        key = self.keyvar.get()
        ok = False
        if len(key) < 1:
            self.checklbl.configure(text='Minimum 1 character')
        elif not all(0 <= ord(c) <= 255 for c in key):
            self.checklbl.configure(text='Only latin1 characters allowed')
        else:
            self.checklbl.configure(text='Key OK')
            ok = True
            self.key = key
        self.ok.configure(state='normal' if ok else 'disabled')
        return ok


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky=NSEW)
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.create_widgets()
        self.plainbox.focus()
        self.keys = defaultdict(lambda: None)

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        # Row 0
        tk.Label(self, text='Plaintext').grid(columnspan=3)
        # Rows 1-2
        plainbox = tk.Text(self, height=5, undo=True)
        plainbox.grid(rowspan=2, sticky=NSEW)
        self.plainbox = plainbox
        plainscroll = tk.Scrollbar(self, orient='vertical',
                                   command=plainbox.yview)
        plainscroll.grid(row=1, rowspan=2, column=1, sticky=NSEW)
        plainbox.configure(yscrollcommand=plainscroll.set)
        plainload = tk.Button(self, text='Load', command=self.load_plain)
        plainload.grid(row=1, column=2)
        plainsave = tk.Button(self, text='Save', command=self.save_plain)
        plainsave.grid(row=2, column=2)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        # Row 3
        container = tk.Frame(self)
        container.grid(columnspan=2, sticky=NSEW)
        for i in range(3):
            container.columnconfigure(i, weight=1)
        encrypt = tk.Button(container, text='\u2193 Encrypt!',
                                 command=self.encrypt)
        encrypt.grid(row=0, column=0)
        decrypt = tk.Button(container, text='\u2191 Decrypt!',
                                 command=self.decrypt)
        decrypt.grid(row=0, column=1)
        clear = tk.Button(container, text='Clear!', command=self.clear)
        clear.grid(row=0, column=2)
        # Row 4
        tk.Label(self, text='Ciphertext').grid(columnspan=3)
        # Rows 5-6
        cipherbox = tk.Text(self, height=5, undo=True)
        cipherbox.grid(rowspan=2, sticky=NSEW)
        self.cipherbox = cipherbox
        cipherscroll = tk.Scrollbar(self, orient='vertical',
                                    command=cipherbox.yview)
        cipherbox.configure(yscrollcommand=cipherscroll.set)
        cipherscroll.grid(row=5, rowspan=2, column=1, sticky=NSEW)
        cipherload = tk.Button(self, text='Load', command=self.load_cipher)
        cipherload.grid(row=5, column=2)
        ciphersave = tk.Button(self, text='Save', command=self.save_cipher)
        ciphersave.grid(row=6, column=2)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        # All along the right column
        algoframe = tk.Frame(self)
        algoframe.grid(row=0, rowspan=7, column=3, sticky=tk.N)
        tk.Label(algoframe, text='Cipher selection').grid()
        self.algo_selection = tk.StringVar()
        self.algo_selection.set('vs')
        tk.Radiobutton(algoframe, variable=self.algo_selection, value='vs',
                       text='Vigen\xe8re Cipher').grid(sticky=tk.W)
        tk.Radiobutton(algoframe, variable=self.algo_selection, value='vf',
                       text='Full Vigen\xe8re').grid(sticky=tk.W)
        tk.Radiobutton(algoframe, variable=self.algo_selection, value='va',
                       text='Autokey Vigen\xe8re').grid(sticky=tk.W)
        tk.Radiobutton(algoframe, variable=self.algo_selection, value='ve',
                       text='Extended Vigen\xe8re').grid(sticky=tk.W)
        tk.Radiobutton(algoframe, variable=self.algo_selection, value='p',
                       text='Playfair Cihper').grid(sticky=tk.W)
        tk.Radiobutton(algoframe, variable=self.algo_selection, value='s',
                       text='Superencryption').grid(sticky=tk.W)
        tk.Radiobutton(algoframe, variable=self.algo_selection, value='a',
                       text='Affine Cipher').grid(sticky=tk.W)
        tk.Radiobutton(algoframe, variable=self.algo_selection, value='h',
                       text='Hill Cipher').grid(sticky=tk.W)
        tk.Radiobutton(algoframe, variable=self.algo_selection, value='e',
                       text='Enigma M4').grid(sticky=tk.W)
        setkey = tk.Button(algoframe, text='Set key', command=self.set_key)
        setkey.grid()

    def clear(self):
        self.plainbox.delete('1.0', 'end')
        self.plainbox.edit('reset')
        self.cipherbox.delete('1.0', 'end')
        self.cipherbox.edit('reset')

    def set_key(self):
        window = tk.Toplevel(self)
        algo = self.algo_selection.get()
        def use_key(key):
            self.keys[algo] = key
            #print(algo, key)
        current = self.keys[algo]
        if algo == 'vs' or algo == 'va':
            keywin = VigenereKey(('Autokey ' if algo == 'va' else '')
                                 + 'Vigen\xe8re Key',
                                 current, use_key, window)
        elif algo == 've':
            keywin = ExtendedVigenereKey(current, use_key, window)

    def encrypt(self):
        print(self.algo_selection.get())
        print(repr(self.plainbox.get('1.0', 'end')))
        self.cipherbox.delete('1.0', 'end')
        self.cipherbox.insert('end', 'ash nazg durbatuluk')
        self.cipherbox.edit('reset')
        print('Conspicuously pretending to encrypt!')

    def decrypt(self): pass

    def load_plain(self): pass
    def save_plain(self): pass
    def load_cipher(self): pass
    def save_cipher(self): pass


def main():
    app = Application()
    app.master.title('Encryptor/Decryptor')
    app.mainloop()


if __name__ == '__main__':
    main()
