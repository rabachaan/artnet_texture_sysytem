import bisect
import logging
import TimeCode  # TimeCodeモジュールを利用

# ログの設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TCsection:
    def __init__(self):
        """
        セクションデータを初期化する
        """
        self.sectionData: list[dict[str, any]] = []  # 開始フレームと終了フレームを含む形式で管理

    def __str__(self) -> str:
        """
        クラスインスタンスをprintで表示するときの文字列表現を定義
        """
        if not self.sectionData:
            return "No sections available."
        
        result = "Sections:\n"
        for section in self.sectionData:
            result += f"  - Name: {section['name']}, Start: {section['start_timecode']}, End: {section['end_timecode']}\n"
        return result

    def initialize_sections(self) -> None:
        """
        セクションデータをリセットする
        """
        self.sectionData = []
        logging.info("Section data has been initialized.")

    def add_section(self, section_name: str, start_timecode: str, end_timecode: str) -> None:
        """
        セクションを追加する（二分探索を活用しソートを維持）
        """
        start_frame = TimeCode.calcTotalFrame(start_timecode)
        end_frame = TimeCode.calcTotalFrame(end_timecode)

        if start_frame >= end_frame:
            raise ValueError(f"Section '{section_name}' has start timecode later than or equal to end timecode.")

        # 挿入位置を特定
        idx = bisect.bisect_left([s["start"] for s in self.sectionData], start_frame)

        # 重複チェック（前後のセクションのみ確認）
        if idx > 0 and self.sectionData[idx - 1]["end"] > start_frame:
            raise ValueError(f"Section '{section_name}' overlaps with the previous section.")
        if idx < len(self.sectionData) and self.sectionData[idx]["start"] < end_frame:
            raise ValueError(f"Section '{section_name}' overlaps with the next section.")

        # ソートされたリストに挿入
        self.sectionData.insert(idx, {
            "name": section_name,
            "start": start_frame,
            "end": end_frame,
            "start_timecode": start_timecode,
            "end_timecode": end_timecode,
        })
        logging.info(f"Section '{section_name}' has been added successfully.")

    def find_section(self, timecode_input:int):
        """
        二分探索を使用して、指定されたタイムコードに該当するセクションを検索する
        """
        #total_frame = TimeCode.calcTotalFrame(timecode_input)

        total_frame = timecode_input
        # 二分探索で候補を見つける
        idx = bisect.bisect_right([s["start"] for s in self.sectionData], total_frame) - 1
        if idx >= 0 and self.sectionData[idx]["start"] <= total_frame < self.sectionData[idx]["end"]:
            return self.sectionData[idx]["name"]

        return None

    def remove_section(self, section_name: str) -> None:
        """
        指定したセクションを削除する
        """
        self.sectionData = [s for s in self.sectionData if s["name"] != section_name]
        logging.info(f"Section '{section_name}' has been removed.")

    def add_multiple_sections(self, sections: list[dict[str, str]]) -> None:
        """
        複数のセクションを一括で追加する
        """
        for section in sections:
            try:
                self.add_section(section["name"], section["start"], section["end"])
            except ValueError as e:
                logging.error(f"Failed to add section '{section['name']}': {e}")
                print(f"Error: {e}")
