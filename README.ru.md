# SvgCompress

## Описание

`SvgCompress` — это инструмент для сжатия SVG-файлов путём удаления ненужных пробелов, комментариев, метаданных и некоторых других данных. Также поддерживается оптимизация с помощью [SVGO](https://github.com/svg/svgo) и сжатие в [SVGZ](https://ru.wikipedia.org/wiki/SVG#SVGZ). Утилита помогает уменьшить размер файла, очистить SVG-файлы для большей производительности и подготовить их к выпуску.

## Установка

1. **Клонирование репозитория:**

    ```sh
    git clone https://github.com/pasabanov/SvgCompress
    cd SvgCompress
    ```

2. **(Опционально) Если вы хотите использовать опцию `--svgo`, убедитесь, что [SVGO](https://github.com/svg/svgo) установлен.**

3. **(Опционально) Если вы хотите использовать опцию `--svgz`, убедитесь, что [gzip](https://www.gnu.org/software/gzip/) установлен.**

## Использование

Чтобы сжать SVG-файлы, выполните скрипт с помощью следующей команды:

```sh
python compress-svg.py [options] paths
```

## Опции

`-h`, `--help` Показать это сообщение и выйти  
`-v`, `--version` Показать версию скрипта  
`-r`, `--recursive` Обрабатывать директории рекурсивно  
`-f`, `--remove-fill` Удалить атрибуты `fill="..."`   
`--svgo` Использовать [SVGO](https://github.com/svg/svgo), если он установлен в системе  
`--svgz` Сжать в формат [.svgz](https://ru.wikipedia.org/wiki/SVG#SVGZ) с помощью утилиты [gzip](https://www.gnu.org/software/gzip/) после обработки  
`--no-default` Не выполнять оптимизаций по умолчанию (если вы хотите использовать только [SVGO](https://github.com/svg/svgo), [gzip](https://www.gnu.org/software/gzip/) или оба)

## Примеры
1. Сжать один SVG-файл:
    ```sh
    python compress-svg.py my-icon.svg
    ```
2. Сжать все SVG-файлы в указанных директориях и файлах:
    ```sh
    python compress-svg.py my-icons-directory1 my-icon.svg directory2 icon2.svg
    ```
3. Сжать все SVG-файлы в директории и её поддиректориях:
    ```sh
    python compress-svg.py -r my-icons-directory
   ```
4. Сжать SVG-файл и удалить все атрибуты `fill="..."` (сделать картинку моноцветной):
    ```sh
    python compress-svg.py -f my-icon.svg
    ```
5. Сравнить размеры файлов до и после сжатия с помощью `ls-sizes.py`:
    ```sh
    cp -r icons/ compressed-icons/
    python compress-svg.py [options] compressed-icons
    python ls-sizes.py
    ```

## Лицензия

This project is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

For more details, see the full license at https://creativecommons.org/licenses/by/4.0/

## Авторские права
2024 Пётр Александрович Сабанов