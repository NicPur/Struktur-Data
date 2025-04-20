import pandas as pd

def load_dataset(filepath):
    df = pd.read_excel(filepath)
    df.columns = df.columns.str.strip().str.lower()
    return df

def linear_search(data, column, keyword):
    result = []
    for index, row in data.iterrows():
        if str(keyword).lower() in str(row[column]).lower():
            result.append(row)
    return result

def binary_search(data, column, keyword):
    data = data.copy()

    if column == "tahun terbit":
        try:
            keyword = int(keyword)
            data[column] = pd.to_numeric(data[column], errors='coerce').fillna(0).astype(int)
        except ValueError:
            print("Keyword tahun tidak valid. Harus berupa angka.")
            return []
    else:
        data[column] = data[column].astype(str).str.lower()
        keyword = keyword.lower()

    sorted_data = data.sort_values(by=column).reset_index(drop=True)
    left = 0
    right = len(sorted_data) - 1
    results = []

    while left <= right:
        mid = (left + right) // 2
        mid_value = sorted_data.at[mid, column]

        if keyword == mid_value:
            results.append(sorted_data.loc[mid])
            l = mid - 1
            while l >= 0 and sorted_data.at[l, column] == keyword:
                results.insert(0, sorted_data.loc[l])
                l -= 1
            r = mid + 1
            while r < len(sorted_data) and sorted_data.at[r, column] == keyword:
                results.append(sorted_data.loc[r])
                r += 1
            break
        elif keyword < mid_value:
            right = mid - 1
        else:
            left = mid + 1

    return results

def display_results(results):
    if not results:
        print("Data tidak ditemukan.")
    else:
        print(f"\nDitemukan {len(results)} hasil:")
        for i, row in enumerate(results, start=1):
            print("\n" + "="*40)
            print(f"[{i}] Judul Paper    : {row.get('judul paper', 'Tidak tersedia')}")
            tahun = row.get('tahun terbit', 'Tidak tersedia')
            if isinstance(tahun, float) and tahun.is_integer():
                tahun = int(tahun)
            print(f"    Tahun Terbit   : {tahun}")
            print(f"    Nama Penulis   : {row.get('nama penulis', 'Tidak tersedia')}")
            print(f"    Nama Mahasiswa : {row.get('nama mahasiswa', 'Tidak tersedia')}")
            print(f"    Link Paper     : {row.get('link paper', 'Tidak tersedia')}")
        print("="*40)

def main():
    file_path = r"C:\Users\NICO\Downloads\Struktur_Data_Dataset_Kelas_A_B_C.xlsx"
    data = load_dataset(file_path)

    while True:
        print("\n=== Pencarian Dataset Paper ===")
        print("1. Judul Paper")
        print("2. Tahun Terbit")
        print("3. Nama Penulis")
        print("4. Keluar")
        kolom_opsi = input("Cari berdasarkan (1/2/3/4): ")

        if kolom_opsi == "4":
            print("Program selesai. Terima kasih.")
            break

        kolom = "judul paper"
        if kolom_opsi == "2":
            kolom = "tahun terbit"
        elif kolom_opsi == "3":
            kolom = "nama penulis"

        metode = input("Gunakan metode pencarian (linear/binary): ").strip().lower()
        keyword = input("Masukkan keyword: ").strip()

        if metode == "linear":
            hasil = linear_search(data, kolom, keyword)
        elif metode == "binary":
            hasil = binary_search(data, kolom, keyword)
        else:
            print("Metode pencarian tidak dikenali.")
            continue

        display_results(hasil)

if __name__ == "__main__":
    main()
