import tkinter as tk
import tkinter.simpledialog
import tkinter.filedialog
import tkinter.ttk
from collections import defaultdict
import string
import random
import numpy as np
import Tucil1 as Kripto


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
        keytxt = tk.Entry(self, textvariable=self.keyvar)
        keytxt.bind('<KeyPress-Return>', self.enter)
        keytxt.grid(columnspan=2, sticky=NSEW)
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
        keytxt.configure(validate='focus', validatecommand=self.check)
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
            key = key.upper()
            self.keyvar.set(key)
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


class FullVigenereKey(VigenereKey):
    def __init__(self, current_key, key_callback, master=None):
        super().__init__('Full Vigen\xe8re Key', None, key_callback,
                         master)
        if current_key is not None:
            alphakey, tbl = current_key
            self.keyvar.set(alphakey)
            self.set_tbl('\n'.join(''.join(r) for r in tbl))
            self.check() # also sets key
        else:
            alphakey, tbl = None, None
            self.key = (None, None)

    def create_widgets(self, title):
        # Row 0
        tk.Label(self, text=title).grid(columnspan=2)
        # Row 1
        self.keyvar = tk.StringVar()
        keytxt = tk.Entry(self, textvariable=self.keyvar)
        keytxt.bind('<KeyPress-Return>', self.enter)
        keytxt.grid(columnspan=2, sticky=NSEW)
        keytxt.focus()
        # Row 2
        tk.Label(self, text='Tabula Recta').grid(columnspan=2)
        # Row 3
        std = tk.Button(self, text='Generate standard', command=self.gen_std)
        std.grid()
        rnd = tk.Button(self, text='Generate random', command=self.gen_rnd)
        rnd.grid(row=3, column=1)
        # Row 4
        tbltxt = tk.Text(self, width=26, height=26)
        tbltxt.grid(columnspan=2)
        self.tbltxt = tbltxt
        # Row 5
        checklbl = tk.Label(self)
        checklbl.grid(columnspan=2)
        self.checklbl = checklbl
        # Row 6
        check = tk.Button(self, text='Check', command=self.check)
        check.grid()
        ok = tk.Button(self, text='Ok', command=self.submit, state='disabled')
        ok.bind('<KeyPress-Return>', self.enter)
        ok.grid(row=6, column=1)
        self.ok = ok
        keytxt.configure(validate='focus', validatecommand=self.check)
        self.check()

    def set_tbl(self, tbl):
        self.tbltxt.delete('1.0', 'end')
        self.tbltxt.insert('end', tbl)

    def gen_std(self):
        row = string.ascii_uppercase
        tbl = ''
        for i in range(26):
            if i > 0: tbl += '\n'
            tbl += row
            row = row[1:] + row[:1]
        self.set_tbl(tbl)

    def gen_rnd(self):
        tbl = ''
        row = list(string.ascii_uppercase)
        for i in range(26):
            if i > 0: tbl += '\n'
            random.shuffle(row)
            tbl += ''.join(row)
        self.set_tbl(tbl)

    def check(self):
        def checkme(alphakey, tbl):
            if len(alphakey) < 1:
                self.checklbl.configure(text='Minimum 1 letter')
                return False
            if not all(c in string.ascii_letters for c in alphakey):
                self.checklbl.configure(text='Only letters A-Z allowed')
                return False
            # Check table
            rows = tbl.upper().split()
            if len(rows) != 26 or not all(len(r) == 26 for r in rows):
                self.checklbl.configure(text='Table must be 26x26')
                return False
            parsed_tbl = [list(r) for r in rows]
            alphaset = set(string.ascii_uppercase)
            for row in parsed_tbl:
                if set(row) != alphaset:
                    self.checklbl.configure(
                        text='Each row must be a permutation of A-Z')
                    return False
            self.checklbl.configure(text='Key OK')
            alphakey = alphakey.upper()
            valid_tbl = '\n'.join(''.join(r) for r in parsed_tbl)
            if tbl != valid_tbl:
                self.set_tbl(valid_tbl)
            self.keyvar.set(alphakey)
            self.key = (alphakey, parsed_tbl)
            return True
        #print('checking', self.keyvar.get())
        alphakey = self.keyvar.get()
        tbl = self.tbltxt.get('1.0', 'end')
        ok = checkme(alphakey, tbl)
        self.ok.configure(state='normal' if ok else 'disabled')
        return ok


class AffineKey(VigenereKey):
    # Integers coprime to 26
    VALID_M = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

    def __init__(self, current_key, key_callback, master=None):
        super().__init__('Affine Key', None, key_callback, master)
        if current_key is not None:
            m, b = current_key
            self.mcbb.set(str(m))
            self.bvar.set(str(b))
            self.check()
        else:
            alphakey, tbl = None, None
            self.key = (None, None)

    def create_widgets(self, title):
        # Row 0
        tk.Label(self, text=title).grid(columnspan=2)
        # Row 1
        tk.Label(self, text='m').grid()
        tk.Label(self, text='b').grid(row=1, column=1)
        # Row 2
        mcbb = tk.ttk.Combobox(self, values=self.VALID_M)
        mcbb.bind('<KeyPress-Return>', self.enter)
        mcbb.grid(sticky=NSEW)
        mcbb.focus()
        self.mcbb = mcbb
        self.bvar = tk.StringVar()
        btxt = tk.Spinbox(self, textvariable=self.bvar, to=25, increment=1)
        btxt['from'] = 0
        btxt.bind('<KeyPress-Return>', self.enter)
        btxt.grid(row=2, column=1)
        # Row 3
        checklbl = tk.Label(self)
        checklbl.grid(columnspan=2)
        self.checklbl = checklbl
        # Row 4
        check = tk.Button(self, text='Check', command=self.check)
        check.grid()
        ok = tk.Button(self, text='Ok', command=self.submit, state='disabled')
        ok.bind('<KeyPress-Return>', self.enter)
        ok.grid(row=4, column=1)
        self.ok = ok
        btxt.configure(validate='focus', validatecommand=self.check)
        self.check()

    def check(self):
        def checkme(mstr, bstr):
            if len(mstr) < 1 or len(bstr) < 1:
                self.checklbl.configure(text='Please enter both values')
                return False
            try:
                m = int(mstr)
                b = int(bstr)
            except ValueError:
                self.checklbl.configure(text='Only digits 0-9 allowed')
                return False
            m = m % 26
            b = b % 26
            if m not in self.VALID_M:
                self.checklbl.configure(text='m must be coprime to 26')
                return False
            self.mcbb.set(str(m))
            self.bvar.set(str(b))
            self.checklbl.configure(text='Key OK')
            self.key = (m, b)
            return True
        mstr = self.mcbb.get()
        bstr = self.bvar.get()
        ok = checkme(mstr, bstr)
        self.ok.configure(state='normal' if ok else 'disabled')
        return ok


class HillKey(VigenereKey):
    def __init__(self, current_key, key_callback, master=None):
        super().__init__('Hill Key', None, key_callback,
                         master)
        if current_key is not None:
            self.key = current_key
            self.set_tbl(self.textlify(self.key))
            self.check() # also sets key
        else:
            self.key = None

    def create_widgets(self, title):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        # Row 0
        tk.Label(self, text=title).grid(columnspan=2)
        # Row 1
        tk.Label(self, text='Matrix').grid(columnspan=2)
        # Row 2
        tbltxt = tk.Text(self, width=5, height=5)
        tbltxt.grid(columnspan=2, sticky=NSEW)
        self.tbltxt = tbltxt
        # Row 3
        tk.Label(self, text='Dimension').grid()
        self.dimvar = tk.StringVar()
        tk.Entry(self, textvariable=self.dimvar, state='readonly')\
            .grid(row=3, column=1)
        # Row 4
        checklbl = tk.Label(self)
        checklbl.grid(columnspan=2)
        self.checklbl = checklbl
        # Row 5
        check = tk.Button(self, text='Check', command=self.check)
        check.grid()
        ok = tk.Button(self, text='Ok', command=self.submit, state='disabled')
        ok.bind('<KeyPress-Return>', self.enter)
        ok.grid(row=5, column=1)
        self.ok = ok
        self.check()

    def textlify(self, tbl):
        return '\n'.join(' '.join(map(str, r)) for r in tbl)

    def set_tbl(self, tbl):
        self.tbltxt.delete('1.0', 'end')
        self.tbltxt.insert('end', tbl)

    def check(self):
        def checkme(tbl):
            if len(tbl) < 1:
                self.checklbl.configure(text='Please enter a square matrix')
                return False
            if not all(c in (string.digits + ' \n') for c in tbl):
                self.checklbl.configure(text='Only digits and spaces allowed')
                return False
            # Check table
            rows = [r.split() for r in tbl.splitlines()]
            dim = len(rows)
            self.dimvar.set(str(dim))
            if not all(len(r) == dim for r in rows):
                self.checklbl.configure(text='Matrix must be square')
                return False
            try:
                parsed_tbl = [[int(x) for x in r] for r in rows]
            except ValueError:
                self.checklbl.configure(text='Numbers not understood')
                return False
            mat = np.array(parsed_tbl)
            assert mat.shape[0] == mat.shape[1]
            det = np.around(np.linalg.det(mat))
            if det == 0:
                self.checklbl.configure(text='Matrix is singular')
                return False
            try:
                inv_det = Kripto.modInverse(det, 26)
            except Exception:
                self.checklbl.configure(text='Determinant is not invertible')
                return False
            self.checklbl.configure(text='Key OK')
            valid_tbl = self.textlify(mat)
            if tbl != valid_tbl:
                self.set_tbl(valid_tbl)
            self.key = mat
            return True
        tbl = self.tbltxt.get('1.0', 'end').strip()
        ok = checkme(tbl)
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
        for i in range(4):
            container.columnconfigure(i, weight=1)
        encrypt = tk.Button(container, text='\u2193 Encrypt!',
                                 command=self.encrypt)
        encrypt.grid(row=0, column=1)
        self.group_chars = tk.StringVar()
        self.group_chars.set('0')
        groupck = tk.Checkbutton(container, text='Group output',
                                 variable=self.group_chars)
        groupck.grid(row=0, column=0)
        decrypt = tk.Button(container, text='\u2191 Decrypt!',
                                 command=self.decrypt)
        decrypt.grid(row=0, column=2)
        clear = tk.Button(container, text='Clear!', command=self.clear)
        clear.grid(row=0, column=3)
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
                       text='Enigma M4', state='disabled').grid(sticky=tk.W)
        setkey = tk.Button(algoframe, text='Set key', command=self.set_key)
        setkey.grid()

    def clear(self):
        self.plainbox.delete('1.0', 'end')
        self.plainbox.edit('reset')
        self.cipherbox.delete('1.0', 'end')
        self.cipherbox.edit('reset')

    # Tk cannot handle embedded NULLs, so we encode it as an extra-ASCII char
    @staticmethod
    def encode_bytes_for_display(data):
        return data.replace('\0', '\u2400')

    @staticmethod
    def decode_bytes_from_display(data):
        return data.replace('\u2400', '\0')

    def set_plain(self, plain):
        self.plainbox.delete('1.0', 'end')
        self.plainbox.insert('end', self.encode_bytes_for_display(plain))
        self.plainbox.edit('reset')

    def get_plain(self):
        txt = self.plainbox.get('1.0', 'end')
        return self.decode_bytes_from_display(txt[:-1]) # skip last line ending

    def set_cipher(self, cipher):
        self.cipherbox.delete('1.0', 'end')
        self.cipherbox.insert('end', self.encode_bytes_for_display(cipher))
        self.cipherbox.edit('reset')

    def get_cipher(self):
        txt = self.cipherbox.get('1.0', 'end')
        return self.decode_bytes_from_display(txt[:-1]) # skip last line ending

    def set_key(self):
        window = tk.Toplevel(self)
        algo = self.algo_selection.get()
        def use_key(key):
            self.keys[algo] = key
            print(algo, key)
        current = self.keys[algo]
        if algo == 'vs' or algo == 'va':
            VigenereKey(('Autokey ' if algo == 'va' else '')
                        + 'Vigen\xe8re Key',
                        current, use_key, window)
        elif algo == 've':
            ExtendedVigenereKey(current, use_key, window)
        elif algo == 'vf':
            FullVigenereKey(current, use_key, window)
        elif algo == 'p':
            VigenereKey('Playfair Key', current, use_key, window)
        elif algo == 's':
            VigenereKey('Superencryption Key', current, use_key, window)
        elif algo == 'a':
            AffineKey(current, use_key, window)
        elif algo == 'h':
            HillKey(current, use_key, window)
        else:
            window.destroy()
            tk.simpledialog.messagebox.showerror(
                'Not implemented',
                'Sorry, this cipher is not implemented yet.')

    def encrypt(self):
        algo = self.algo_selection.get()
        key = self.keys[algo]
        ungroup = self.group_chars.get() == '0'
        if key is None:
            tk.simpledialog.messagebox.showinfo(
                'No key', 'Please set the key first')
            return
        plain = self.get_plain()
        if algo == 'vs':
            cipher = Kripto.VigenereEncrypt(plain, key)
            if ungroup: cipher = ''.join(cipher.split())
        elif algo == 'vf':
            cipher = Kripto.FullVigenereC(plain, key[0], key[1])
            if ungroup: cipher = ''.join(cipher.split())
        elif algo == 'va':
            cipher = Kripto.AutoKeyVigenereEncrypt(plain, key)
            if ungroup: cipher = ''.join(cipher.split())
        elif algo == 've':
            cipher = Kripto.ExtendedVigenereEncrypt(plain, key)
        elif algo == 'p':
            ptbl = Kripto.playfairTable('', key)
            cipher = ''.join(Kripto.PlayfairC(ptbl, plain, ''))
            if not ungroup: cipher = Kripto.ArrangeEncription(cipher)
        elif algo == 's':
            cipher = Kripto.SuperEncrypt(plain, key)
            if ungroup: cipher = ''.join(cipher.split())
        elif algo == 'a':
            cipher = Kripto.affineCipherEncrypt(plain, key[0], key[1])
            if ungroup: cipher = ''.join(cipher.split())
        elif algo == 'h':
            cipher = Kripto.hillCipherEncrypt(plain, key.shape[0], key)
            if ungroup: cipher = ''.join(cipher.split())
        else:
            tk.simpledialog.messagebox.showerror(
                'Not implemented',
                'Sorry, this cipher is not implemented yet.')
            return
        self.set_cipher(cipher)

    def decrypt(self):
        algo = self.algo_selection.get()
        key = self.keys[algo]
        if key is None:
            tk.simpledialog.messagebox.showinfo(
                'No key', 'Please set the key first')
            return
        cipher = self.get_cipher()
        if algo == 'vs':
            plain = Kripto.VigenereDecrypt(cipher, key)
        elif algo == 'vf':
            plain = Kripto.FullVigenereDecrypt(cipher, key[0], key[1])
        elif algo == 'va':
            plain = Kripto.AutoKeyVigenereDecrypt(cipher, key)
        elif algo == 've':
            plain = Kripto.ExtendedVigenereDecrypt(cipher, key)
        elif algo == 'p':
            if len(cipher) % 2 != 0:
                tk.simpledialog.messagebox.showerror(
                    'Invalid ciphertext',
                    'Ciphertext length must be a multiple of 2')
                return
            ptbl = Kripto.playfairTable('', key)
            plain = Kripto.PlayfairDecrypt(ptbl,
                                           Kripto.ArrangeText(cipher.lower()))
        elif algo == 's':
            plain = Kripto.SuperDecrypt(cipher, key)
        elif algo == 'a':
            plain = Kripto.affineCipherDecrypt(cipher, key[0], key[1])
        elif algo == 'h':
            m = key.shape[0]
            if len(cipher) % m != 0:
                tk.simpledialog.messagebox.showerror(
                    'Invalid ciphertext',
                    'Ciphertext length must be a multiple of {}.'.format(m))
                return
            plain = Kripto.hillCipherDecrypt(cipher, m, key)
        else:
            tk.simpledialog.messagebox.showerror(
                'Not implemented',
                'Sorry, this cipher is not implemented yet.')
            return
        self.set_plain(plain)

    def load_plain(self):
        self.set_plain(self.load_file())

    def save_plain(self):
        self.save_file(self.get_plain())

    def load_cipher(self):
        self.set_cipher(self.load_file())

    def save_cipher(self):
        self.save_file(self.get_cipher())

    def load_file(self):
        f = tk.filedialog.askopenfile(mode='rb', parent=self)
        data = f.read().decode('latin1')
        f.close()
        return data

    def save_file(self, data):
        f = tk.filedialog.asksaveasfile(mode='wb', parent=self)
        f.write(data.encode('latin1'))
        f.close()


def main():
    app = Application()
    app.master.title('Encryptor/Decryptor')
    app.mainloop()


if __name__ == '__main__':
    main()
